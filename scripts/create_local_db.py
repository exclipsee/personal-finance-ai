"""Create a local SQLite database at ./finance.db with the project's tables.

This script intentionally ignores DATABASE_URL and creates a local sqlite
database for development/testing so the `run_agent.py summarize` command
can run against a local DB without needing Docker or Postgres.
"""
from __future__ import annotations

from pathlib import Path
import sys
from sqlalchemy import create_engine

# Ensure the repository root is on sys.path so imports like `db.models`
# work when running this script from `scripts/`.
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from db import models


def main() -> None:
    engine = create_engine("sqlite:///./finance.db", future=True)
    models.Base.metadata.create_all(bind=engine)
    print("Created local SQLite database ./finance.db with tables.")


if __name__ == "__main__":
    main()
