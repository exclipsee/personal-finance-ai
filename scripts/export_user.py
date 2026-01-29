"""Export all data for a given user to JSON (transactions + feedback).

Usage: python scripts/export_user.py --username demo --out demo_export.json
"""
from __future__ import annotations

from pathlib import Path
import json
import sys
import argparse

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from db.database import SessionLocal
from db.models import User, Transaction, CategoryFeedback


def export_user(username: str, out_path: Path) -> None:
    session = SessionLocal()
    try:
        user = session.query(User).filter_by(username=username).first()
        if not user:
            print(f"User not found: {username}")
            return

        txs = [
            {
                "id": t.id,
                "date": str(t.date),
                "description": t.description,
                "amount": t.amount,
                "category": t.category,
                "created_at": str(t.created_at),
            }
            for t in user.transactions
        ]

        feedback = [
            {
                "id": f.id,
                "transaction_id": f.transaction_id,
                "old_category": f.old_category,
                "new_category": f.new_category,
                "created_at": str(f.created_at),
            }
            for f in session.query(CategoryFeedback).filter_by(user_id=user.id)
        ]

        payload = {"user": {"id": user.id, "username": user.username, "email": user.email}, "transactions": txs, "feedback": feedback}
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(payload, indent=2))
        print(f"Exported user data to {out_path}")
    finally:
        session.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--username", required=True)
    parser.add_argument("--out", default="exports/user_export.json")
    args = parser.parse_args()
    export_user(args.username, Path(args.out))


if __name__ == "__main__":
    main()
