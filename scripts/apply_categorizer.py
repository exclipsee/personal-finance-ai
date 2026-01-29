"""Apply trained categorizer to unlabeled transactions (CLI)."""
from __future__ import annotations

from pathlib import Path
import argparse
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from db.database import SessionLocal
from ingest.categorizer import apply_predictions


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="models/categorizer.joblib")
    parser.add_argument("--limit", type=int, default=200)
    args = parser.parse_args()

    session = SessionLocal()
    try:
        n = apply_predictions(session, Path(args.model), limit=args.limit)
        print(f"Applied predictions to {n} transactions.")
    finally:
        session.close()


if __name__ == "__main__":
    main()
