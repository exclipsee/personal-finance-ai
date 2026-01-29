"""CLI to import CSV files into the local DB using `ingest.csv_import`.

Example:
  python scripts/import_csv.py data/sample_transactions.csv --bank chase
"""
from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from ingest.csv_import import normalize_and_insert
from db.database import SessionLocal


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="Path to CSV file")
    parser.add_argument("--bank", help="Optional bank template name (e.g., chase)")
    args = parser.parse_args()

    path = Path(args.path)
    if not path.exists():
        print(f"File not found: {path}")
        return

    inserted = normalize_and_insert(str(path), SessionLocal, bank=args.bank)
    print(f"Inserted {inserted} transactions from {path}")


if __name__ == "__main__":
    main()
