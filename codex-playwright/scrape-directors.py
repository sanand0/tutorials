#!/usr/bin/env python3
"""Command-line entrypoint that delegates to scrape_directors.main."""

import typer

from scrape_directors import main


if __name__ == "__main__":
    typer.run(main)
