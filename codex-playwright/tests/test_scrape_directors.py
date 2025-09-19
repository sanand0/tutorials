from pathlib import Path

import pytest

from scrape_directors import extract_director_bio, parse_top_directors

FIXTURES = Path(__file__).resolve().parent.parent / "fixtures"


def read_fixture(name: str) -> str:
    return (FIXTURES / name).read_text(encoding="utf-8")


def test_parse_top_directors_selects_expected_top_five() -> None:
    html = read_fixture("best_director.html")
    entries = parse_top_directors(html, top_n=5, seed=0)
    names = [entry["name"] for entry in entries]
    assert names == [
        "John Ford",
        "Frank Capra",
        "William Wyler",
        "Steven Spielberg",
        "George Stevens",
    ]
    assert all(entry["wins"] >= entries[-1]["wins"] for entry in entries)
    assert entries[0]["relative_url"] == "/wiki/John_Ford"


def test_extract_director_bio_normalizes_infobox_and_summary() -> None:
    html = read_fixture("john_ford.html")
    record = extract_director_bio(html)

    assert record["name"] == "John Ford"
    assert record["summary"].startswith("John Martin Feeney")

    infobox = record["infobox"]
    assert "February 1, 1894" in infobox["born"]
    assert "Cape Elizabeth" in infobox["born"]
    assert infobox["born"].startswith("February")
    assert infobox["died"].startswith("August 31, 1973")
    occupations = infobox["occupations"].split('; ')
    assert 'Film director' in occupations
    assert any(item.lower() == 'producer' for item in occupations)
    assert infobox["years_active"] == "1913–1966"
    assert "Mary McBride Smith" in infobox["spouse"]

    for value in infobox.values():
        assert "[" not in value, value
