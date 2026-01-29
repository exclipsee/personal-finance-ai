"""CLI for submitting category feedback for a transaction.

Example:
  python scripts/feedback_cli.py --tx 123 --new "Groceries" --user demo
"""
from __future__ import annotations

from pathlib import Path
import argparse
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from db.database import SessionLocal
from db.models import CategoryFeedback, Transaction, User


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tx", type=int, required=True, help="Transaction ID")
    parser.add_argument("--new", required=True, help="New category label")
    parser.add_argument("--user", help="Username submitting feedback")
    args = parser.parse_args()

    session = SessionLocal()
    try:
        tx = session.query(Transaction).get(args.tx)
        if not tx:
            print("Transaction not found")
            return
        user = None
        if args.user:
            user = session.query(User).filter_by(username=args.user).first()

        fb = CategoryFeedback(transaction_id=tx.id, user_id=(user.id if user else None), old_category=tx.category, new_category=args.new)
        session.add(fb)
        # also apply new category to the transaction immediately
        tx.category = args.new
        session.commit()
        print(f"Recorded feedback for tx {tx.id}: {args.new}")
    finally:
        session.close()


if __name__ == "__main__":
    main()
