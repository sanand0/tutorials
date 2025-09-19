# Playwright Best Director Scraper

This repository contains a Playwright-powered scraper that finds the Academy Award for Best Director winners with the most wins, visits each director’s biography page, normalizes their infobox details, and exports the enriched data to `top-directors.csv`.

## Repository Prompts

This repository was generated using these 3 prompts on Codex CLI:

```
Use Playwright to:

- Find the top 5 directors who got the most best-director Academy Awards by scraping https://en.wikipedia.org/wiki/Academy_Award_for_Best_Director. (Pick randomly for tie-breakers).
- For each, go through their bio page and extract bio details for each.
  - Think of a logical structure that will capture all relevant information for them
- Write a Python script `scrape-directors.py` that will extract this information from any director's page
- Run it for the top 5 directors' pages and save the results in a top-directors.csv

Write unit tests for this.
```

```
Generate a README.md documenting
- What this repo does and how to use it
- The prompt used to generate it
- How you (Codex CLI) used playwright to generate the script (use your conversation history + thinking for this)
- How this process can be extended to generate scrapers for any content from any site
- What worked well and what didn't - and therefore, what best practices to follow.
```

```
Expand the `## How Codex CLI Built This with Playwright` section into much more detail,
explaining step-by-step how Codex worked to solve this problem.
Look at the logs and cite verbatim from conversation history.
```

## Using the Scraper

1. Install dependencies and browsers (first run only):
   ```bash
   UV_CACHE_DIR=.uv-cache uv run playwright install firefox
   ```
2. Run the scraper (defaults to top 5 directors, seed 0, Firefox):
   ```bash
   UV_CACHE_DIR=.uv-cache uv run python scrape-directors.py --limit 5 --seed 0 --output top-directors.csv
   ```
3. Execute the tests:
   ```bash
   UV_CACHE_DIR=.uv-cache uv run --extra dev pytest
   ```

The resulting `top-directors.csv` contains cleaned infobox fields plus a JSON snapshot of the full infobox per director. All logic lives in `scrape_directors.py`; `scrape-directors.py` is the Typer entrypoint.

## How Codex CLI Built This with Playwright

1. **Prepared the toolchain and browser runtime.** Encountered sandboxed install failures, then requested elevated access to install Playwright and its Firefox build.
   > UV_CACHE_DIR=.uv-cache uv run playwright install firefox

   When a network block interrupted dependency resolution, the CLI surfaced the exact error before retrying with approval.
   > error: Failed to fetch: `https://pypi.org/simple/pytest/`

2. **Captured source HTML for reliable offline parsing.** After an initial locator timeout, saved the full awards page HTML for inspection.
   > page.goto('https://en.wikipedia.org/wiki/Academy_Award_for_Best_Director', wait_until='domcontentloaded')
   > Path('fixtures').mkdir(exist_ok=True)
   > Path('fixtures/best_director.html').write_text(html, encoding='utf-8')

   Repeated the pattern for director biographies to compare infobox layouts without repeated network calls.
   > page.goto(url, wait_until='domcontentloaded')
   > Path(f'fixtures/{name}.html').write_text(page.content(), encoding='utf-8')

3. **Reverse-engineered the awards table structure.** Probed the cached HTML with `lxml` to confirm how wins propagate down the rowspan and to derive deterministic tie-handling.
   > table_nodes = doc.xpath("//h3[@id='Multiple_wins']/parent::div/following-sibling::table[1]")
   > result = [('John Ford', 4), ('Frank Capra', 3), ('William Wyler', 3), ('Steven Spielberg', 2), ('George Stevens', 2)]

4. **Refined infobox cleaning logic.** Verified that replacing `remove` with `drop_tree()` preserved trailing text (e.g., birth dates) while stripping hidden spans.
   > cleaned: <td class="infobox-data"><br>February 1, 1894<br><div style="display:inline" class="birthplace"><a href="/wiki/Cape_Elizabeth,_Maine" title="Cape Elizabeth, Maine">Cape Elizabeth, Maine</a>, U.S.</div></td>
   > ['February 1, 1894', 'Cape Elizabeth, Maine', ', U.S.']

5. **Codified expected behaviour with tests.** Wrote pytest cases that lock in the top-five selection and cleaned infobox fields before finalizing the implementation.
   > entries = parse_top_directors(html, top_n=5, seed=0)
   > assert names == [
   >     "John Ford",
   >     "Frank Capra",
   >     "William Wyler",
   >     "Steven Spielberg",
   >     "George Stevens",
   > ]

6. **Implemented the reusable scraper and CLI wrapper.** Consolidated parsing, scraping, and CSV-writing logic, then connected it to a Typer entrypoint.
   > records = _scrape_top_directors(limit, seed)
   > typer.run(main)

7. **Executed the live scrape and exported the dataset.** Ran the finished workflow end-to-end to produce the CSV deliverable.
   > UV_CACHE_DIR=.uv-cache uv run python scrape-directors.py --limit 5 --seed 0 --output top-directors.csv

These steps combined Playwright’s navigation with `lxml` parsing, fixture-driven iteration, and seeded randomness to deliver a reproducible scraper.

## Extending the Pattern to Other Sites

1. Identify the target listing page and capture representative HTML fixtures with Playwright to avoid hammering the live site while iterating.
2. Draft parsing helpers against the fixture using `lxml`/CSS selectors until the data model is stable.
3. Encode the workflow into composable functions: index parser, detail parser, export routine.
4. Wrap it in a small Typer/CLI layer, parameterizing things like seed, limit, output location, and optionally browser choice.
5. Add pytest coverage combining fixtures and unit-level assertions so regressions surface before live runs.

## What Worked Well

- **Fixtures first:** Saving HTML locally let us iterate quickly without repeated network trips or flaky selectors.
- **Deterministic randomness:** Using an injectable seed kept tie-breaking reproducible and testable.
- **Incremental REPL checks:** Quick `uv run python - <<'PY'` snippets exposed parsing bugs (e.g., `drop_tree` vs. `remove`) before they reached the tests.
- **Separated concerns:** Parsing helpers, scraping orchestration, and CLI entry were isolated, keeping the happy path readable.

## Pitfalls and Best Practices

- Removing nodes with `getparent().remove()` dropped trailing text (lost birth dates). Switching to `drop_tree()` preserved tails—prefer it when cleaning HTML trees.
- Network sandboxing required explicit escalations; cache downloads where possible to minimize interactive approvals.
- Typer expects the module to be importable—without a thin wrapper, `uv run scrape-directors.py` failed. Always confirm CLI ergonomics.
- Wikipedia markup varies; tests should tolerate reasonable variations (e.g., occupation casing) instead of asserting exact strings.

Following these practices makes it straightforward to adapt the approach to scrape other structured or semi-structured web data with Playwright and Python.
