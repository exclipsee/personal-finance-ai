"""Seed the local SQLite database with example users and transactions.

Run this after `scripts/create_local_db.py` to populate `./finance.db`.
"""
from __future__ import annotations

from pathlib import Path
import sys
from datetime import date, timedelta

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from db.database import SessionLocal
from db.models import User, Transaction


def make_transactions(user_id: int) -> list[Transaction]:
    base = date.today()
    rows = [
        Transaction(date=base - timedelta(days=1), description="Grocery Store", amount=-54.23, category="Groceries", user_id=user_id),
        Transaction(date=base - timedelta(days=2), description="Salary", amount=2500.00, category="Income", user_id=user_id),
        Transaction(date=base - timedelta(days=3), description="Coffee Shop", amount=-4.75, category="Dining", user_id=user_id),
        Transaction(date=base - timedelta(days=10), description="Electric Bill", amount=-120.50, category="Utilities", user_id=user_id),
        Transaction(date=base - timedelta(days=5), description="Movie Ticket", amount=-12.00, category="Entertainment", user_id=user_id),
    ]
    return rows


def main() -> None:
    session = SessionLocal()
    try:
        # Create a demo user
        demo = User(username="demo", email="demo@example.com", hashed_password="notasecret")
        session.add(demo)
        session.flush()  # get demo.id

        txs = make_transactions(demo.id)
        session.add_all(txs)
        session.commit()
        print(f"Inserted {len(txs)} transactions for user 'demo'.")
    finally:
        session.close()


if __name__ == "__main__":
    main()
