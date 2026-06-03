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
MONTHS = ["january", "february", "march", "april", "may", "june", "july",
          "august", "september", "october", "november", "december"]
# DMS typed meeting dates a dozen ways. meeting_year() extracts the 4-digit
# year from a title in any of them, or returns None if the title carries no
# date (a plain article). Used to fold dated minutes under a year-grouped node.
_MONTH_RE = r"(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)"
_DATE_PATTERNS = [
    # (regex, group index for the 4-digit year)
    (re.compile(r"\b(?:19|20)\d{4,}\b"), 0),                                  # YYYYMMDD / YYYYMM / typo'd long runs
    (re.compile(r"\b\d{4}((?:19|20)\d{2})\b"), 1),                            # MMDDYYYY
    (re.compile(r"\b(?:19|20)\d{2}[-/.\s]\d{1,2}[-/.\s]\d{1,2}\b"), 0),       # YYYY-M-D (any sep incl. space)
    (re.compile(r"\b\d{1,2}[-/.\s]\d{1,2}[-/.\s]((?:19|20)\d{2})\b"), 1),     # M-D-YYYY
    (re.compile(r"\b(?:19|20)\d{2}\s+" + _MONTH_RE, re.I), 0),                # YYYY Monthname
    (re.compile(_MONTH_RE + r"[a-z]*\.?\s+\d{0,2},?\s*((?:19|20)\d{2})\b", re.I), 1),  # Monthname ... YYYY
    (re.compile(r"\b\d{1,2}[-/.]\d{1,2}[-/.](\d{2})\b"), "yy"),               # M-D-YY (2-digit year)
]


def meeting_year(title: str) -> str | None:
    for pat, grp in _DATE_PATTERNS:
        m = pat.search(title)
        if not m:
            continue
        if grp == "yy":
            return "20" + m.group(1)
        return m.group(grp)[:4] if grp == 0 else m.group(grp)
    return None
MEETING_SUBGROUP_ORDER = [
    "Board & Committee Meetings", "Meetings by Year",
    "Meetings by Month", "Statements of Intent",
]


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

    # tree: group -> subgroup(None|str) -> slug -> {"label", "pages": [(label,path)]}
    tree: dict = collections.defaultdict(
        lambda: collections.defaultdict(lambda: collections.defaultdict(
            lambda: {"label": "", "pages": []})))
    for e in entries:
        group = group_for(e["slug"])
        sub = subgroup_for(group, e["slug"])
        node = tree[group][sub][e["slug"]]
        node["label"] = e["category"]
        node["pages"].append((e["page_label"], e["path"]))

    def emit_pages(pages, indent):
        """Emit a category's pages: plain articles directly, dated meeting
        minutes collapsed under a year-grouped 'Meeting Minutes' node."""
        content, minutes = [], []
        for plabel, path in pages:
            yr = meeting_year(plabel)
            (minutes if yr else content).append((plabel, path, yr))
        out = []
        for plabel, path, _ in sorted(content, key=lambda p: p[0].lower()):
            out.append(f'{" " * indent}- "{esc(plabel)}": {path}')
        if not minutes:
            return out

        years = sorted({y for _, _, y in minutes}, reverse=True)

        def emit_years(ind):
            o = []
            for yr in years:
                o.append(f'{" " * ind}- "{yr}":')
                rows = sorted([(l, p) for l, p, y in minutes if y == yr],
                              key=lambda r: r[0].lower())
                for l, p in rows:
                    o.append(f'{" " * (ind + 2)}- "{esc(l)}": {p}')
            return o

        if content:
            # Mixed category: keep articles up top, tuck minutes behind a node.
            out.append(f'{" " * indent}- "Meeting Minutes":')
            out += emit_years(indent + 2)
        elif len(years) > 1:
            # Pure-minutes category spanning years: group by year directly.
            out += emit_years(indent)
        else:
            # Pure-minutes, single year (e.g. "2010 Meetings"): flat list.
            for l, p in sorted([(l, p) for l, p, _ in minutes],
                               key=lambda r: r[0].lower()):
                out.append(f'{" " * indent}- "{esc(l)}": {p}')
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
            ordered = [s for s in MEETING_SUBGROUP_ORDER if s in subs]
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
