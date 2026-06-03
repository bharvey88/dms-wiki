# Dallas Makerspace Wiki — MkDocs Material proof of concept

An **unofficial proof-of-concept** that mirrors the [Dallas Makerspace wiki](https://dallasmakerspace.org/)
into a [MkDocs Material](https://squidfunk.github.io/mkdocs-material/) site to show how the
content looks and reads in a modern docs theme.

**Live demo:** https://bharvey88.github.io/dms-wiki/

This is not affiliated with or endorsed by Dallas Makerspace. Wiki content is
licensed [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/); see [LICENSE](LICENSE).

## How it works

The whole site is generated from the live wiki by one script:

```
scripts/build_docs.py     # the conversion engine
scripts/lib/              # pure, unit-tested helpers (slugify, link rewriting, HTML cleanup)
scripts/mkdocs.base.yml   # theme/branding config (no nav)
docs/                     # generated markdown — committed so the site is browsable and deploys are deterministic
mkdocs.yml                # = mkdocs.base.yml + a generated nav, written by the script
```

The script:

1. Enumerates every content article via the MediaWiki API.
2. Fetches each page's server-rendered HTML, strips MediaWiki chrome (edit links, the built-in TOC), and converts it to Markdown with pandoc.
3. Rewrites internal `/wiki/Page` links to relative paths; links to non-mirrored pages fall back to the live wiki. Images are hot-linked back to dallasmakerspace.org.
4. Groups pages into folders by their first wiki category and writes a Material-friendly navigation tree.

CI (`.github/workflows/deploy.yml`) only builds and deploys the committed `docs/` — it does **not** re-run the scrape.

## Re-running the mirror

```bash
python -m pip install -r requirements.txt
python scripts/build_docs.py            # full mirror
python scripts/build_docs.py --limit 25 # quick sample for spot-checking
mkdocs serve                            # preview at http://127.0.0.1:8000
```

## Tests

```bash
python -m pytest scripts/tests
```
