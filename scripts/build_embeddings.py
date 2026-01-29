"""Build embeddings for transactions and persist a local vector store.

Usage:
  python scripts/build_embeddings.py --provider auto
"""
from __future__ import annotations

from pathlib import Path
import argparse
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from db.database import SessionLocal
from ingest.embeddings import build_embeddings


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--provider", default="auto", help="openai or tfidf or auto")
    args = parser.parse_args()

    session = SessionLocal()
    try:
        path = build_embeddings(session, out_dir=Path("models"), provider=args.provider)
        print(f"Built embeddings and saved to {path}")
    finally:
        session.close()


if __name__ == "__main__":
    main()
