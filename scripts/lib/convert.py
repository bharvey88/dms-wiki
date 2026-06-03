"""Pure helpers for the Dallas Makerspace wiki -> MkDocs conversion.

These functions have no network or filesystem side effects so they can be
unit-tested in isolation. The orchestration lives in build_docs.py.
"""
from __future__ import annotations

import posixpath
import re
import unicodedata
from urllib.parse import unquote

HOST = "https://dallasmakerspace.org"

# MediaWiki namespaces we never mirror; links to these go to the live wiki.
NAMESPACE_PREFIXES = (
    "File:", "Image:", "Media:", "Category:", "Special:", "Help:",
    "Template:", "Template_talk:", "User:", "User_talk:", "Talk:",
    "Project:", "MediaWiki:", "Portal:",
)


def slugify(text: str) -> str:
    """Filesystem- and URL-safe slug: ascii, lowercase, hyphen-separated."""
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-") or "untitled"


def normalize_title(title: str) -> str:
    """Canonicalize a wiki title for map lookups.

    MediaWiki treats spaces and underscores as equivalent and the first
    character as case-insensitive (rest is case-sensitive).
    """
    title = unquote(title).replace("_", " ").strip()
    if not title:
        return title
    return title[0].upper() + title[1:]


def pretty_label(title: str) -> str:
    """Human-friendly label from a wiki title or category name."""
    return unquote(title).replace("_", " ").strip()


def is_namespaced(title: str) -> bool:
    """True if the title belongs to a namespace we don't mirror."""
    norm = title.replace(" ", "_")
    return any(norm.startswith(p) for p in NAMESPACE_PREFIXES)


def parse_wiki_href(href: str):
    """Parse an href.

    Returns one of:
      ("internal", title, anchor)  -> a /wiki/ link to a content page
      ("namespaced", absolute_url) -> a /wiki/ link to a non-mirrored namespace
      ("absolute", absolute_url)   -> a site-relative link that should hot-link
      None                         -> leave the href untouched (external/anchor)
    """
    if not href:
        return None
    # In-page anchor only
    if href.startswith("#"):
        return None
    # Already external
    if href.startswith("http://") or href.startswith("https://") or href.startswith("mailto:"):
        return None
    # Protocol-relative -> external
    if href.startswith("//"):
        return None
    if href.startswith("/wiki/"):
        rest = href[len("/wiki/"):]
        anchor = ""
        if "#" in rest:
            rest, anchor = rest.split("#", 1)
        if is_namespaced(rest):
            return ("namespaced", HOST + href)
        return ("internal", normalize_title(rest), anchor)
    # Any other site-relative path (/w/..., /index.php, etc.) -> hot-link
    if href.startswith("/"):
        return ("absolute", HOST + href)
    return None


def md_relpath(from_doc: str, to_doc: str) -> str:
    """Relative link between two doc paths (POSIX, relative to docs root).

    Both args are paths under docs/ like "classes/foo.md". Returns a link
    MkDocs resolves correctly, e.g. "../teaching/bar.md".
    """
    from_dir = posixpath.dirname(from_doc)
    rel = posixpath.relpath(to_doc, from_dir or ".")
    return rel


def absolutize_asset(src: str) -> str:
    """Turn a wiki-relative image/src URL into an absolute hot-link."""
    if src.startswith("//"):
        return "https:" + src
    if src.startswith("/"):
        return HOST + src
    return src
