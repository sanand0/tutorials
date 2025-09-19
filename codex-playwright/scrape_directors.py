from __future__ import annotations

import csv
import random
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

import orjson
from lxml import html
from playwright.sync_api import sync_playwright

WIKIPEDIA_BASE = "https://en.wikipedia.org"
BEST_DIRECTOR_URL = f"{WIKIPEDIA_BASE}/wiki/Academy_Award_for_Best_Director"
FIELD_ALIASES = {
    "born": "born",
    "birth name": "birth_name",
    "died": "died",
    "resting place": "resting_place",
    "occupation": "occupations",
    "occupations": "occupations",
    "years active": "years_active",
    "spouse": "spouse",
    "spouses": "spouse",
    "partner": "partner",
    "domestic partner": "partner",
    "children": "children",
    "awards": "awards",
    "notable works": "notable_works",
    "notable work": "notable_works",
    "alma mater": "alma_mater",
}
CSV_FIELD_ORDER = [
    "name",
    "wins",
    "url",
    "summary",
    "birth_name",
    "born",
    "died",
    "resting_place",
    "occupations",
    "years_active",
    "spouse",
    "partner",
    "children",
    "awards",
    "notable_works",
    "alma_mater",
    "infobox_json",
]
CITATION_RE = re.compile(r"\s*\[[^\]]+\]")
NON_WORD_RE = re.compile(r"[^0-9a-z]+")


@dataclass(frozen=True)
class DirectorEntry:
    """Awards table entry."""

    name: str
    wins: int
    relative_url: str


def _clean_text(value: str) -> str:
    if not value:
        return ""
    text = value.replace("\xa0", " ").replace("\u200b", "")
    text = text.replace("\n", " ").replace("·", ";")
    text = CITATION_RE.sub("", text)
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"(?:;\s*)+", "; ", text)
    return text.strip(" ;,\n")


def _clean_fragment(value: str) -> str:
    return _clean_text(value)


def _finalize_list(parts: Iterable[str]) -> str:
    items = [part for part in (_clean_fragment(p) for p in parts) if part]
    if not items:
        return ""
    merged = "; ".join(items)
    merged = re.sub(r"(;\s*){2,}", "; ", merged)
    return merged.strip(" ;,")


def _normalize_label(label: str) -> str:
    if not label:
        return ""
    lowered = label.lower()
    if lowered in FIELD_ALIASES:
        return FIELD_ALIASES[lowered]
    key = NON_WORD_RE.sub("_", lowered).strip("_")
    return key


def _parse_infobox(table: html.HtmlElement) -> dict[str, str]:
    info: dict[str, str] = {}
    for row in table.xpath(".//tr"):
        headers = row.xpath("./th")
        cells = row.xpath("./td")
        if not headers or not cells:
            continue
        label = _clean_fragment(" ".join(headers[0].itertext()))
        if not label:
            continue
        key = _normalize_label(label)
        cell = cells[0]
        for node in cell.xpath(".//style|.//script|.//sup|.//*[contains(@style,'display:none')]"):
            node.drop_tree()
        if key == "born":
            birth_names: list[str] = []
            for nick in cell.xpath(".//*[contains(@class,'nickname')]"):
                birth_text = _finalize_list(nick.itertext())
                if birth_text:
                    birth_names.append(birth_text)
                nick.drop_tree()
            if birth_names and "birth_name" not in info:
                info["birth_name"] = "; ".join(dict.fromkeys(birth_names))
        if key == "spouse":
            for ch in cell.xpath(".//*[contains(@class,'marriage-display-inline')]//sup"):
                ch.drop_tree()
        list_items = cell.xpath(".//li")
        if list_items:
            value = _finalize_list([" ".join(li.itertext()) for li in list_items])
        else:
            value = _finalize_list(cell.itertext())
        info[key] = value
    return info


def parse_top_directors(page_html: str, top_n: int = 5, seed: int | None = 0) -> list[dict[str, Any]]:
    """Parse the multiple-wins table and choose the requested directors."""

    if top_n <= 0:
        return []
    doc = html.fromstring(page_html)
    nodes = doc.xpath("//h3[@id='Multiple_wins']/parent::div/following-sibling::table[1]")
    if not nodes:
        raise ValueError("Could not locate multiple wins table")
    table = nodes[0]
    rows = table.xpath(".//tr")[1:]
    entries: list[DirectorEntry] = []
    current_wins: int | None = None
    for row in rows:
        cells = row.xpath("./td")
        if not cells:
            continue
        name_cell = cells[-1]
        if len(cells) == 2:
            wins_text = _clean_fragment(cells[0].text_content())
            digits = re.sub(r"[^0-9]", "", wins_text)
            if digits:
                current_wins = int(digits)
        if current_wins is None:
            continue
        name = _clean_text(name_cell.text_content())
        if not name:
            continue
        hrefs = name_cell.xpath(".//a/@href")
        relative_url = hrefs[0] if hrefs else ""
        entries.append(DirectorEntry(name=name, wins=current_wins, relative_url=relative_url))
    if not entries:
        return []
    grouped: dict[int, list[DirectorEntry]] = {}
    for entry in entries:
        grouped.setdefault(entry.wins, []).append(entry)
    wins_sorted = sorted(grouped.keys(), reverse=True)
    rng = random.Random(seed) if seed is not None else random
    selected: list[DirectorEntry] = []
    for wins in wins_sorted:
        if len(selected) >= top_n:
            break
        bucket = grouped[wins]
        remaining = top_n - len(selected)
        if len(bucket) <= remaining:
            selected.extend(bucket)
            continue
        chosen = rng.sample(bucket, remaining)
        selected.extend(chosen)
    trimmed = selected[:top_n]
    return [
        {"name": entry.name, "wins": entry.wins, "relative_url": entry.relative_url}
        for entry in trimmed
    ]


def extract_director_bio(page_html: str) -> dict[str, Any]:
    """Extract the cleaned summary plus infobox details."""

    doc = html.fromstring(page_html)
    infobox_nodes = doc.xpath("//table[contains(@class,'infobox')][1]")
    if not infobox_nodes:
        raise ValueError("Director infobox missing")
    infobox = _parse_infobox(infobox_nodes[0])
    name_nodes = infobox_nodes[0].xpath(".//tr[th[contains(@class,'infobox-above')]]//text()")
    if not name_nodes:
        name_nodes = doc.xpath("//h1[@id='firstHeading']/text()")
    name = _clean_text(" ".join(name_nodes))
    summary_nodes = doc.xpath("//div[@id='mw-content-text']//p[normalize-space()][1]")
    summary = _clean_text(summary_nodes[0].text_content()) if summary_nodes else ""
    return {"name": name, "summary": summary, "infobox": infobox}


def _fetch_html(url: str) -> str:
    with sync_playwright() as pw:
        browser = pw.firefox.launch()
        page = browser.new_page()
        page.goto(url, wait_until="domcontentloaded")
        content = page.content()
        browser.close()
    return content


def _scrape_top_directors(limit: int, seed: int) -> list[dict[str, Any]]:
    with sync_playwright() as pw:
        browser = pw.firefox.launch()
        page = browser.new_page()
        page.goto(BEST_DIRECTOR_URL, wait_until="domcontentloaded")
        top_entries = parse_top_directors(page.content(), top_n=limit, seed=seed)
        records: list[dict[str, Any]] = []
        for entry in top_entries:
            url = f"{WIKIPEDIA_BASE}{entry['relative_url']}"
            page.goto(url, wait_until="domcontentloaded")
            bio = extract_director_bio(page.content())
            records.append({
                "name": bio["name"],
                "wins": entry["wins"],
                "url": url,
                "summary": bio["summary"],
                "infobox": bio["infobox"],
            })
        browser.close()
    return records


def _rows_for_csv(records: list[dict[str, Any]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for record in records:
        infobox = record["infobox"]
        row = {
            "name": record["name"],
            "wins": str(record["wins"]),
            "url": record["url"],
            "summary": record["summary"],
        }
        for field in CSV_FIELD_ORDER:
            if field in row:
                continue
            value = infobox.get(field, "")
            row[field] = value
        row["infobox_json"] = orjson.dumps(infobox, option=orjson.OPT_SORT_KEYS).decode()
        rows.append(row)
    return rows


def _write_csv(rows: list[dict[str, str]], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELD_ORDER)
        writer.writeheader()
        writer.writerows(rows)


def main(limit: int = 5, seed: int = 0, output: Path = Path("top-directors.csv")) -> None:
    """Fetch the awards list, enrich biographies, and save a CSV."""

    records = _scrape_top_directors(limit, seed)
    rows = _rows_for_csv(records)
    _write_csv(rows, output)


if __name__ == "__main__":
    import typer

    typer.run(main)
