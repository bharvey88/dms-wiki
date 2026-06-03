#!/usr/bin/env python
"""Mirror the Dallas Makerspace wiki into MkDocs Material markdown.

Pipeline:
  1. Enumerate every content article (namespace 0) via the MediaWiki API.
  2. Fetch each page's server-rendered HTML + categories.
  3. Choose each page's most-specific category as its folder (balanced nav).
  4. Clean MediaWiki chrome, rewrite links/images, convert HTML -> Markdown (pandoc).
  5. Write docs/, a landing page, and mkdocs.yml (base config + generated nav).

Run:  python scripts/build_docs.py [--limit N] [--delay SECONDS]
"""
from __future__ import annotations

import argparse
import collections
import glob
import json
import os
import re
import shutil
import sys
import time
from urllib.parse import unquote

import requests
from bs4 import BeautifulSoup
import pypandoc

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "lib"))
import convert  # noqa: E402

API = "https://dallasmakerspace.org/w/api.php"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DOCS = os.path.join(ROOT, "docs")
BASE_YML = os.path.join(HERE, "mkdocs.base.yml")
OUT_YML = os.path.join(ROOT, "mkdocs.yml")
EXTRA_CSS_SRC = os.path.join(HERE, "extra.css")
# slug -> pretty category label, persisted so the nav can be regenerated
# (`--nav-only`) without re-scraping the wiki.
CATEGORY_LABELS_JSON = os.path.join(HERE, "category_labels.json")

# MkDocs reserves the "templates" directory name (it is excluded from the
# build), so any wiki category that slugifies to a reserved name is suffixed.
RESERVED_DIRS = {"templates"}

UNCATEGORIZED = "Uncategorized"

# Source wiki content can contain embedded API keys/secrets (e.g. a Google Maps
# key in a staticmap URL). Redact them so the mirror never republishes them.
SECRET_PATTERNS = [
    re.compile(r"AIza[0-9A-Za-z_\-]{35}"),       # Google API keys
    re.compile(r"(?i)(api[_-]?key=)[0-9A-Za-z_\-]{16,}"),  # generic key= params
]


def redact_secrets(text: str) -> str:
    for pat in SECRET_PATTERNS:
        if pat.groups:
            text = pat.sub(r"\1REDACTED", text)
        else:
            text = pat.sub("REDACTED_API_KEY", text)
    return text

# MediaWiki chrome to drop before conversion.
STRIP_SELECTORS = [
    ".mw-editsection", "#toc", ".toc", ".noprint", ".mw-empty-elt",
    ".navbox", ".vertical-navbox", ".metadata", ".mw-jump-link",
    "style", "script", "link",
]

# Semantic tags pandoc maps cleanly to Markdown; everything else (div, span,
# section, ...) gets unwrapped so it doesn't survive as raw HTML.
KEEP_TAGS = {
    "p", "a", "img", "h1", "h2", "h3", "h4", "h5", "h6", "ul", "ol", "li",
    "table", "thead", "tbody", "tr", "th", "td", "caption", "b", "strong",
    "i", "em", "u", "s", "code", "pre", "blockquote", "br", "hr", "dl",
    "dt", "dd", "sup", "sub", "abbr", "figure", "figcaption",
}
# Attributes worth keeping, per tag. All others are stripped.
KEEP_ATTRS = {
    "a": {"href"},
    "img": {"src", "alt"},
    "td": {"colspan", "rowspan"},
    "th": {"colspan", "rowspan"},
}


def make_session() -> requests.Session:
    s = requests.Session()
    s.headers["User-Agent"] = (
        "dms-wiki-poc/1.0 (https://github.com/bharvey88/dms-wiki; "
        "mkdocs migration proof of concept)"
    )
    return s


def api_get(session: requests.Session, params: dict) -> dict:
    params = {**params, "format": "json", "formatversion": "2"}
    for attempt in range(4):
        try:
            r = session.get(API, params=params, timeout=30)
            r.raise_for_status()
            return r.json()
        except Exception as exc:  # noqa: BLE001 - retry then surface
            if attempt == 3:
                raise
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError("unreachable")


def enumerate_articles(session, limit: int | None) -> list[str]:
    titles: list[str] = []
    params = {
        "action": "query", "list": "allpages", "apnamespace": 0,
        "aplimit": 500, "apfilterredir": "nonredirects",
    }
    while True:
        data = api_get(session, params)
        for p in data["query"]["allpages"]:
            titles.append(p["title"])
        if "continue" in data:
            params.update(data["continue"])
        else:
            break
    titles.sort(key=str.lower)
    if limit:
        titles = titles[:limit]
    return titles


def fetch_page(session, title: str) -> dict | None:
    data = api_get(session, {
        "action": "parse", "page": title, "prop": "text|categories",
        "redirects": 1, "disableeditsection": 1,
    })
    if "error" in data or "parse" not in data:
        return None
    parse = data["parse"]
    cats = [
        c["category"] for c in parse.get("categories", [])
        if not c.get("hidden")
    ]
    return {"title": parse["title"], "html": parse["text"], "categories": cats}


def choose_category(cats: list[str], freq: collections.Counter) -> str:
    """Pick the most specific (least common) category as the page's folder."""
    if not cats:
        return UNCATEGORIZED
    # Lowest frequency wins; ties broken alphabetically for determinism.
    return min(cats, key=lambda c: (freq[c], c.lower()))


def assign_paths(records: list[dict], freq: collections.Counter) -> dict:
    """Assign each record an output path; return title -> path map.

    Mutates each record with 'category' and 'path'. Paths are POSIX,
    relative to docs/, e.g. "classes/so-you-want-to-teach-a-class.md".
    """
    used: dict[str, set] = collections.defaultdict(set)
    title_to_path: dict[str, str] = {}
    for rec in records:
        category = choose_category(rec["categories"], freq)
        folder = convert.slugify(category)
        if folder in RESERVED_DIRS:
            folder = f"{folder}-category"
        base = convert.slugify(rec["title"])
        slug = base
        n = 2
        while slug in used[folder]:
            slug = f"{base}-{n}"
            n += 1
        used[folder].add(slug)
        path = f"{folder}/{slug}.md"
        rec["category"] = category
        rec["path"] = path
        title_to_path[convert.normalize_title(rec["title"])] = path
    return title_to_path


def clean_and_rewrite(html: str, current_path: str, title_to_path: dict) -> str:
    soup = BeautifulSoup(html, "lxml")
    for sel in STRIP_SELECTORS:
        for el in soup.select(sel):
            el.decompose()

    # If the body contains an <h1> (MediaWiki "=Heading=" style), demote every
    # heading one level so the injected page title is the only h1 and the
    # hierarchy isn't one level too shallow.
    if soup.find("h1"):
        for level in range(5, 0, -1):
            for h in soup.find_all(f"h{level}"):
                h.name = f"h{level + 1}"

    for a in soup.find_all("a"):
        href = a.get("href")
        parsed = convert.parse_wiki_href(href) if href else None
        if not parsed:
            continue
        kind = parsed[0]
        if kind == "internal":
            _, title, anchor = parsed
            target = title_to_path.get(title)
            if target:
                link = convert.md_relpath(current_path, target)
                if anchor:
                    link += "#" + convert.slugify(unquote(anchor).replace("_", " "))
                a["href"] = link
            else:
                # Page exists in a link but wasn't mirrored: fall back to live wiki.
                a["href"] = convert.HOST + "/wiki/" + title.replace(" ", "_")
        else:  # "namespaced" or "absolute"
            a["href"] = parsed[1]

    for img in soup.find_all("img"):
        if img.get("src"):
            img["src"] = convert.absolutize_asset(img["src"])

    # Unwrap non-semantic containers (div/span/section/...) so pandoc emits
    # clean Markdown instead of preserving them as raw HTML.
    for el in soup.find_all(True):
        if el.name not in KEEP_TAGS:
            el.unwrap()
        else:
            allowed = KEEP_ATTRS.get(el.name, set())
            for attr in list(el.attrs):
                if attr not in allowed:
                    del el[attr]

    return str(soup)


def to_markdown(html: str) -> str:
    md = pypandoc.convert_text(
        html, to="gfm", format="html",
        extra_args=["--wrap=none"],
    )
    lines = md.split("\n")
    out, blanks = [], 0
    for ln in lines:
        ln = ln.rstrip()
        # Drop pandoc's bare line-break backslashes and list-separator comments.
        if ln in ("\\", "<!-- -->"):
            continue
        # Strip a trailing hard-break backslash (but keep escaped "\\").
        if ln.endswith("\\") and not ln.endswith("\\\\"):
            ln = ln[:-1].rstrip()
        # Collapse runs of >2 blank lines.
        if ln == "":
            blanks += 1
            if blanks > 1:
                continue
        else:
            blanks = 0
        out.append(ln)
    return redact_secrets("\n".join(out).strip()) + "\n"


def write_page(rec: dict, title_to_path: dict) -> None:
    cleaned = clean_and_rewrite(rec["html"], rec["path"], title_to_path)
    body = to_markdown(cleaned)
    out_path = os.path.join(DOCS, *rec["path"].split("/"))
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    title = convert.pretty_label(rec["title"])
    src = convert.HOST + "/wiki/" + rec["title"].replace(" ", "_")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n")
        f.write(
            f'!!! note "Source"\n'
            f"    Mirrored from [{title}]({src}) on the Dallas Makerspace wiki "
            f"(CC BY-SA 3.0).\n\n"
        )
        f.write(body)


# Featured links for the landing page (icon, title, blurb). Resolved against
# the mirrored-title map; any that aren't mirrored are silently skipped.
FEATURED = [
    ("material-gavel", "Rules and Policies", "The rules and policies that keep the space running."),
    ("material-file-document-outline", "Bylaws", "The organization's governing bylaws."),
    ("material-account-group", "Board of Directors", "Who's on the board and what they do."),
    ("material-tools", "Tools", "Equipment available across the makerspace."),
    ("material-school", "So You Want to Teach A Class", "How to propose and run a class at DMS."),
    ("material-hand-wave", "New Member 411", "Everything a new member needs to get started."),
]


def write_index(title_to_path: dict, page_count: int, category_count: int) -> None:
    out = [
        "# Dallas Makerspace Wiki",
        "",
        '!!! warning "Unofficial proof of concept"',
        "    This is an **unofficial** mirror of the "
        "[Dallas Makerspace wiki](https://dallasmakerspace.org/) built to "
        "demonstrate how the content looks in MkDocs Material. It is not "
        "affiliated with or endorsed by Dallas Makerspace. Content is "
        "[CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/).",
        "",
        f"This mirror contains **{page_count} articles** across "
        f"**{category_count} categories**. Press `/` to search, or jump in below.",
        "",
    ]

    cards = []
    for icon, title, blurb in FEATURED:
        path = title_to_path.get(convert.normalize_title(title))
        if not path:
            continue
        cards.append(f"-   :{icon}: **[{title}]({path})**\n\n    {blurb}")
    if cards:
        out += ['<div class="grid cards" markdown>', ""]
        out += [c + "\n" for c in cards]
        out += ["</div>", ""]

    out += [
        "## Browse everything",
        "",
        "Use the tabs in the top navigation (Areas & Committees, Tools, "
        "Classes, Projects, Events, Governance, Meeting Minutes, Archive) "
        "to browse by topic, or search from the box above.",
        "",
    ]
    with open(os.path.join(DOCS, "index.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(out))


# --- Navigation taxonomy -----------------------------------------------------
# 176 wiki categories are too many for a flat sidebar, so each category (by its
# folder slug) is assigned to one of these themed top-level groups (tabs).

GROUP_ORDER = [
    "Areas & Committees",   # default bucket: shops, SIGs, committees
    "Tools & Equipment",
    "Classes",
    "Projects",
    "Events",
    "Governance",
    "Meeting Minutes",
    "Archive",
]
ARCHIVE_CATS = {
    "uncategorized", "outdated", "historical", "archive", "delete", "cleanup",
    "draft", "templates-category", "pages-with-broken-file-links",
    "pages-with-ignored-display-titles",
}
EVENT_CATS = {"annual-events", "completed-events", "big-move-2014",
              "hackathons", "flyers", "food-for-thought"}
CLASS_CATS = {"classes", "class", "class-curriculum", "classroom", "education",
              "teaching", "skillshare", "certifications", "faq", "how-to"}
TOOL_CATS = {"tools", "equipment", "manuals", "infrastructure",
             "systems-and-infrastructure", "suppliers", "computers",
             "parts-files", "standards", "voipserver", "cloud-computing",
             "community-grid", "digital-media-equipment",
             "software-development-equipment", "hardware"}
GOV_CATS = {"dallas-makerspace", "dms-official", "board-of-directors",
            "officers", "financial", "public-relations", "logistics", "secretary"}
# Near-duplicate categories the wiki accumulated over the years; each alias slug
# is folded into a canonical category in the nav (pages keep their files).
CATEGORY_MERGES = {
    "woodshop": "wood-shop",
    "jewelry": "jewelry-small-metals-committee",
    "small-metals": "jewelry-small-metals-committee",
    "software": "software-development",
    "games": "gaming",
    "groups": "interest-groups",
    "logistics-committee": "logistics",
    "vcc-inventory": "vcc",
    "meeting": "meetings",
    "computer-committee-meeting": "computer-committee-meetings",
}
MONTHS = ["january", "february", "march", "april", "may", "june", "july",
          "august", "september", "october", "november", "december"]
# DMS typed meeting dates a dozen ways. meeting_date() extracts (year, month)
# from a title in any of them; meeting_year() returns just the year (or None for
# a plain, undated article). Used to fold dated minutes under year/month nodes.
MONTH_NAMES = ["", "January", "February", "March", "April", "May", "June",
               "July", "August", "September", "October", "November", "December"]
_MONTH_RE = r"(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)"
_MONTH_NUM = {m[:3].lower(): i for i, m in enumerate(MONTH_NAMES) if m}
# A single year's minutes are sub-grouped by month once they exceed this count.
MONTH_NEST_THRESHOLD = 14


def meeting_date(title: str):
    """Return (year, month): year is a 4-char string or None; month is 1-12
    or None. Tries the many date spellings found in the DMS wiki."""
    t, tl = title, title.lower()
    m = re.search(r"\b((?:19|20)\d{2})(\d{2})(\d{2})\b", t)          # YYYYMMDD
    if m:
        return m.group(1), int(m.group(2))
    m = re.search(r"\b((?:19|20)\d{2})[-/.\s](\d{1,2})[-/.\s]\d{1,2}\b", t)  # YYYY-M-D
    if m:
        return m.group(1), int(m.group(2))
    m = re.search(r"\b(\d{1,2})[-/.\s]\d{1,2}[-/.\s]((?:19|20)\d{2})\b", t)  # M-D-YYYY
    if m:
        return m.group(2), int(m.group(1))
    m = re.search(r"\b(\d{2})\d{2}((?:19|20)\d{2})\b", t)            # MMDDYYYY
    if m:
        return m.group(2), int(m.group(1))
    m = re.search(r"\b((?:19|20)\d{2})\s+(" + _MONTH_RE + r")", tl)  # YYYY Monthname
    if m:
        return m.group(1), _MONTH_NUM[m.group(2)]
    m = re.search(r"\b(" + _MONTH_RE + r")[a-z]*\.?\s+\d{0,2},?\s*((?:19|20)\d{2})\b", tl)  # Monthname YYYY
    if m:
        return m.group(2), _MONTH_NUM[m.group(1)]
    m = re.search(r"\b(\d{1,2})[-/.](\d{1,2})[-/.](\d{2})\b", t)     # M-D-YY
    if m:
        return "20" + m.group(3), int(m.group(1))
    m = re.search(r"\b((?:19|20)\d{4,})\b", t)                       # typo'd long run -> year only
    if m:
        return m.group(1)[:4], None
    return None, None


def meeting_year(title: str):
    return meeting_date(title)[0]


# Sub-sections that break the large "Areas & Committees" tab into themes.
AREA_SUBGROUPS = {
    "machine-shop": "Shops & Fabrication", "metal-shop": "Shops & Fabrication",
    "small-metals": "Shops & Fabrication", "wood-shop": "Shops & Fabrication",
    "woodshop": "Shops & Fabrication", "3d-fabrication": "Shops & Fabrication",
    "fabrication": "Shops & Fabrication", "laser": "Shops & Fabrication",
    "plastics": "Shops & Fabrication", "colchester-lathe": "Shops & Fabrication",
    "makery-stores": "Shops & Fabrication",
    "creative-arts": "Arts & Crafts", "glassworks": "Arts & Crafts",
    "jewelry": "Arts & Crafts", "jewelry-small-metals-committee": "Arts & Crafts",
    "printmaking": "Arts & Crafts", "ceramics": "Arts & Crafts",
    "blacksmithing": "Arts & Crafts", "dye-sublimation": "Arts & Crafts",
    "marbling-workshops": "Arts & Crafts",
    "digital-media": "Media & A/V", "av-studio": "Media & A/V",
    "photography": "Media & A/V", "vector": "Media & A/V",
    "electronics": "Technology & Computing", "software": "Technology & Computing",
    "software-development": "Technology & Computing", "programming": "Technology & Computing",
    "embedded-systems": "Technology & Computing", "hacking": "Technology & Computing",
    "infosec": "Technology & Computing", "crypto-sig": "Technology & Computing",
    "civic-hacking": "Technology & Computing", "computer-committee": "Technology & Computing",
    "hackerspace-committee": "Technology & Computing", "codetalk": "Technology & Computing",
    "fusion-360": "Technology & Computing", "vcc": "Technology & Computing",
    "vcc-inventory": "Technology & Computing", "amateur-radio": "Technology & Computing",
    "aerospace": "Vehicles & Aerospace", "automotive": "Vehicles & Aerospace",
    "motorsports-committee": "Vehicles & Aerospace", "remote-control": "Vehicles & Aerospace",
    "science": "Science & Education", "atomic-energy": "Science & Education",
    "stem": "Science & Education", "museum": "Science & Education",
    "edibles": "Science & Education", "food": "Science & Education",
    "tabletop-gaming": "Games", "gaming": "Games", "games": "Games", "pinball": "Games",
}
AREA_DEFAULT_SUB = "Other Committees & Groups"

# Display order of sub-sections within each group.
SUBGROUP_ORDER = {
    "Meeting Minutes": ["Board & Committee Meetings", "Meetings by Year",
                        "Meetings by Month", "Statements of Intent"],
    "Areas & Committees": [
        "Shops & Fabrication", "Arts & Crafts", "Media & A/V",
        "Technology & Computing", "Vehicles & Aerospace", "Science & Education",
        "Games", AREA_DEFAULT_SUB],
}


def group_for(slug: str) -> str:
    if slug in ARCHIVE_CATS:
        return "Archive"
    if "meeting" in slug or "statements-of-intent" in slug:
        return "Meeting Minutes"
    if "project" in slug:
        return "Projects"
    if slug in EVENT_CATS or "event" in slug:
        return "Events"
    if slug in CLASS_CATS:
        return "Classes"
    if slug in TOOL_CATS:
        return "Tools & Equipment"
    if slug in GOV_CATS:
        return "Governance"
    return "Areas & Committees"


def subgroup_for(group: str, slug: str) -> str | None:
    if group == "Areas & Committees":
        return AREA_SUBGROUPS.get(slug, AREA_DEFAULT_SUB)
    if group != "Meeting Minutes":
        return None
    if "statements-of-intent" in slug:
        return "Statements of Intent"
    if re.match(r"^\d{4}-meetings$", slug):
        return "Meetings by Year"
    if re.match(r"^(" + "|".join(MONTHS) + r")-meetings$", slug):
        return "Meetings by Month"
    return "Board & Committee Meetings"


def category_sort_key(subgroup: str | None, slug: str, label: str):
    """Order categories within a (sub)group: years descending, months by
    calendar, everything else alphabetically."""
    if subgroup == "Meetings by Year":
        m = re.match(r"^(\d{4})", slug)
        return (0, -int(m.group(1)) if m else 0, label.lower())
    if subgroup == "Meetings by Month":
        month = slug.split("-")[0]
        return (0, MONTHS.index(month) if month in MONTHS else 99, label.lower())
    return (0, 0, label.lower())


def write_mkdocs_yml(entries: list[dict]) -> None:
    """Build mkdocs.yml = base config + grouped nav.

    entries: list of {slug, category, page_label, path}.
    """
    with open(BASE_YML, encoding="utf-8") as f:
        base = f.read().rstrip() + "\n\n"

    def esc(s):
        return s.replace('"', '\\"')

    # Canonical label per slug, so merged categories show one consistent name.
    slug_label = {}
    for e in entries:
        slug_label.setdefault(e["slug"], e["category"])

    # tree: group -> subgroup(None|str) -> slug -> {"label", "pages": [(label,path)]}
    tree: dict = collections.defaultdict(
        lambda: collections.defaultdict(lambda: collections.defaultdict(
            lambda: {"label": "", "pages": []})))
    for e in entries:
        slug = CATEGORY_MERGES.get(e["slug"], e["slug"])
        group = group_for(slug)
        sub = subgroup_for(group, slug)
        node = tree[group][sub][slug]
        node["label"] = slug_label.get(slug, e["category"])
        node["pages"].append((e["page_label"], e["path"]))

    def emit_pages(pages, indent):
        """Emit a category's pages: plain articles directly, dated meeting
        minutes collapsed under a year-grouped 'Meeting Minutes' node. A single
        year with many minutes is further split by month."""
        content, minutes = [], []
        for plabel, path in pages:
            yr, mo = meeting_date(plabel)
            if yr:
                minutes.append((plabel, path, yr, mo))
            else:
                content.append((plabel, path))
        out = []
        for plabel, path in sorted(content, key=lambda p: p[0].lower()):
            out.append(f'{" " * indent}- "{esc(plabel)}": {path}')
        if not minutes:
            return out

        byyear = collections.defaultdict(list)
        for plabel, path, yr, mo in minutes:
            byyear[yr].append((plabel, path, mo))
        years = sorted(byyear, reverse=True)

        def emit_year_items(items, ind):
            """items: [(label, path, month)] for one year."""
            if len(items) > MONTH_NEST_THRESHOLD:
                bymonth = collections.defaultdict(list)
                for l, p, mo in items:
                    bymonth[mo if (mo and 1 <= mo <= 12) else 0].append((l, p))
                o = []
                for mo in sorted(bymonth, key=lambda x: (x == 0, x)):
                    name = MONTH_NAMES[mo] if mo else "Undated"
                    o.append(f'{" " * ind}- "{name}":')
                    for l, p in sorted(bymonth[mo], key=lambda r: r[0].lower()):
                        o.append(f'{" " * (ind + 2)}- "{esc(l)}": {p}')
                return o
            return [f'{" " * ind}- "{esc(l)}": {p}' for l, p in
                    sorted([(l, p) for l, p, _ in items], key=lambda r: r[0].lower())]

        def emit_years(ind):
            o = []
            for yr in years:
                o.append(f'{" " * ind}- "{yr}":')
                o += emit_year_items(byyear[yr], ind + 2)
            return o

        if content:
            # Mixed category: keep articles up top, tuck minutes behind a node.
            out.append(f'{" " * indent}- "Meeting Minutes":')
            out += emit_years(indent + 2)
        elif len(years) > 1:
            # Pure-minutes category spanning years: group by year directly.
            out += emit_years(indent)
        else:
            # Pure-minutes single year (e.g. "2010 Meetings"): months or flat.
            out += emit_year_items(byyear[years[0]], indent)
        return out

    def emit_categories(slug_map, sub, indent):
        lines = []
        order = sorted(slug_map, key=lambda s: category_sort_key(
            sub, s, slug_map[s]["label"]))
        for slug in order:
            node = slug_map[slug]
            lines.append(f'{" " * indent}- "{esc(node["label"])}":')
            lines += emit_pages(node["pages"], indent + 2)
        return lines

    lines = ["nav:", "  - Home: index.md"]
    for group in GROUP_ORDER:
        if group not in tree:
            continue
        lines.append(f'  - "{group}":')
        subs = tree[group]
        if list(subs) == [None]:
            lines += emit_categories(subs[None], None, 4)
        else:
            pref = SUBGROUP_ORDER.get(group, [])
            ordered = [s for s in pref if s in subs]
            ordered += [s for s in sorted(filter(None, subs)) if s not in ordered]
            for sub in ordered:
                lines.append(f'    - "{esc(sub)}":')
                lines += emit_categories(subs[sub], sub, 6)

    with open(OUT_YML, "w", encoding="utf-8") as f:
        f.write(base)
        f.write("\n".join(lines) + "\n")


def entries_from_records(records: list[dict]) -> list[dict]:
    return [{
        "slug": rec["path"].split("/")[0],
        "category": convert.pretty_label(rec["category"]),
        "page_label": convert.pretty_label(rec["title"]),
        "path": rec["path"],
    } for rec in records]


def entries_from_disk() -> list[dict]:
    """Reconstruct nav entries from the generated docs/ tree (no scrape).

    Page labels come from each file's H1; category labels come from the
    persisted slug->label map (falling back to a prettified slug)."""
    labels = {}
    if os.path.exists(CATEGORY_LABELS_JSON):
        with open(CATEGORY_LABELS_JSON, encoding="utf-8") as f:
            labels = json.load(f)
    entries = []
    for md in glob.glob(os.path.join(DOCS, "*", "*.md")):
        slug = os.path.basename(os.path.dirname(md))
        rel = os.path.relpath(md, DOCS).replace(os.sep, "/")
        with open(md, encoding="utf-8") as f:
            first = f.readline().strip()
        page_label = first[2:].strip() if first.startswith("# ") else slug
        entries.append({
            "slug": slug,
            "category": labels.get(slug, slug.replace("-", " ").title()),
            "page_label": page_label,
            "path": rel,
        })
    return entries


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--limit", type=int, default=None,
                    help="Only convert the first N articles (for spot-checking).")
    ap.add_argument("--delay", type=float, default=0.05,
                    help="Seconds to sleep between page fetches.")
    ap.add_argument("--nav-only", action="store_true",
                    help="Regenerate mkdocs.yml nav from the existing docs/ "
                         "tree without re-scraping the wiki.")
    args = ap.parse_args()

    if args.nav_only:
        entries = entries_from_disk()
        write_mkdocs_yml(entries)
        groups = {group_for(e["slug"]) for e in entries}
        print(f"Rebuilt nav: {len(entries)} pages across "
              f"{len({e['slug'] for e in entries})} categories in "
              f"{len(groups)} groups.", flush=True)
        return 0

    session = make_session()
    print("Enumerating articles...", flush=True)
    titles = enumerate_articles(session, args.limit)
    print(f"  {len(titles)} articles to mirror", flush=True)

    print("Fetching pages...", flush=True)
    records = []
    for i, title in enumerate(titles, 1):
        rec = fetch_page(session, title)
        if rec is None:
            print(f"  [skip] {title} (no content)", flush=True)
            continue
        records.append(rec)
        if i % 50 == 0 or i == len(titles):
            print(f"  {i}/{len(titles)}", flush=True)
        time.sleep(args.delay)

    freq = collections.Counter()
    for rec in records:
        freq.update(rec["categories"])

    title_to_path = assign_paths(records, freq)

    print("Converting to markdown...", flush=True)
    for rec in records:
        write_page(rec, title_to_path)

    cats = len({r["category"] for r in records})
    print("Writing landing page, stylesheet + mkdocs.yml...", flush=True)
    write_index(title_to_path, len(records), cats)
    os.makedirs(os.path.join(DOCS, "stylesheets"), exist_ok=True)
    shutil.copy2(EXTRA_CSS_SRC, os.path.join(DOCS, "stylesheets", "extra.css"))
    entries = entries_from_records(records)
    with open(CATEGORY_LABELS_JSON, "w", encoding="utf-8") as f:
        json.dump({e["slug"]: e["category"] for e in entries}, f,
                  indent=2, sort_keys=True)
    write_mkdocs_yml(entries)

    print(f"Done: {len(records)} pages across {cats} categories.", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
