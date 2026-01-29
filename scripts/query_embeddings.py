"""Query the local embeddings store for similar transactions."""
from __future__ import annotations

from pathlib import Path
import argparse
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from ingest.embeddings import query
from db.database import SessionLocal
from db.models import Transaction


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", required=True, help="Query text")
    parser.add_argument("--top", type=int, default=10)
    args = parser.parse_args()

    res = query(args.q, artifact_path=Path("models/embeddings.joblib"), top_k=args.top)
    session = SessionLocal()
    try:
        for tx_id, dist in res:
            tx = session.query(Transaction).get(tx_id)
            print(f"id={tx_id} dist={dist:.4f} date={tx.date} amount={tx.amount} desc={tx.description} category={tx.category}")
    finally:
        session.close()


if __name__ == "__main__":
    main()
