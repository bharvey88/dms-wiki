import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))

import convert  # noqa: E402


def test_slugify_basic():
    assert convert.slugify("So You Want to Teach A Class") == "so-you-want-to-teach-a-class"


def test_slugify_strips_punctuation_and_accents():
    assert convert.slugify("Café & Crème (v2)!") == "cafe-creme-v2"
    assert convert.slugify("Rules/Policies") == "rules-policies"


def test_slugify_never_empty():
    assert convert.slugify("!!!") == "untitled"


def test_normalize_title_space_underscore_equivalence():
    assert convert.normalize_title("So_You_Want") == convert.normalize_title("So You Want")


def test_normalize_title_capitalizes_first_letter_only():
    assert convert.normalize_title("class_FAQs") == "Class FAQs"


def test_pretty_label():
    assert convert.pretty_label("Dallas_Makerspace") == "Dallas Makerspace"


def test_is_namespaced():
    assert convert.is_namespaced("File:HowtoaddanewClass.pdf")
    assert convert.is_namespaced("Category:Classes")
    assert not convert.is_namespaced("So You Want to Teach A Class")


def test_parse_internal_link():
    kind, title, anchor = convert.parse_wiki_href("/wiki/Class_FAQs")
    assert kind == "internal"
    assert title == "Class FAQs"
    assert anchor == ""


def test_parse_internal_link_with_anchor():
    kind, title, anchor = convert.parse_wiki_href("/wiki/Rules_and_Policies#Honorarium")
    assert kind == "internal"
    assert title == "Rules and Policies"
    assert anchor == "Honorarium"


def test_parse_namespaced_link_goes_to_live_wiki():
    kind, url = convert.parse_wiki_href("/wiki/File:HowtoaddanewClass.pdf")
    assert kind == "namespaced"
    assert url == "https://dallasmakerspace.org/wiki/File:HowtoaddanewClass.pdf"


def test_parse_absolute_site_link():
    kind, url = convert.parse_wiki_href("/w/images/a/ab/foo.png")
    assert kind == "absolute"
    assert url == "https://dallasmakerspace.org/w/images/a/ab/foo.png"


def test_parse_external_and_anchor_left_alone():
    assert convert.parse_wiki_href("https://example.com") is None
    assert convert.parse_wiki_href("//example.com/x") is None
    assert convert.parse_wiki_href("#section") is None
    assert convert.parse_wiki_href("mailto:a@b.com") is None


def test_md_relpath_same_dir():
    assert convert.md_relpath("classes/a.md", "classes/b.md") == "b.md"


def test_md_relpath_cross_dir():
    assert convert.md_relpath("classes/a.md", "teaching/b.md") == "../teaching/b.md"


def test_md_relpath_to_root():
    assert convert.md_relpath("classes/a.md", "index.md") == "../index.md"


def test_absolutize_asset():
    assert convert.absolutize_asset("/w/images/x.png") == "https://dallasmakerspace.org/w/images/x.png"
    assert convert.absolutize_asset("//upload.example/x.png") == "https://upload.example/x.png"
    assert convert.absolutize_asset("https://x/y.png") == "https://x/y.png"
