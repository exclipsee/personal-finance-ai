"""Generate and insert larger synthetic datasets into ./finance.db.

Usage:
  python scripts/seed_more.py --users 10 --tx-per-user 100 --days 365

This script creates `users` demo accounts and `tx_per_user` transactions
each, with random dates, categories and amounts. Commits in batches for
performance.
"""
from __future__ import annotations

from pathlib import Path
import sys
import argparse
import random
from datetime import date, timedelta

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from db.database import SessionLocal
from db.models import User, Transaction


DEFAULT_CATEGORIES = [
    "Groceries",
    "Dining",
    "Utilities",
    "Entertainment",
    "Transport",
    "Health",
    "Income",
    "Rent",
    "Subscriptions",
    "Other",
]


def random_amount(category: str) -> float:
    if category == "Income":
        return round(random.uniform(1500, 5000), 2)
    if category == "Rent":
        return -round(random.uniform(800, 2000), 2)
    # expenses
    return -round(random.uniform(1, 400), 2)


def random_date(days_back: int) -> date:
    return date.today() - timedelta(days=random.randint(0, days_back))


def create_user(session, idx: int) -> User:
    user = User(username=f"user{idx}", email=f"user{idx}@example.com", hashed_password="seeded")
    session.add(user)
    session.flush()
    return user


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--users", type=int, default=10)
    parser.add_argument("--tx-per-user", type=int, default=100)
    parser.add_argument("--days", type=int, default=365)
    parser.add_argument("--batch-size", type=int, default=500)
    args = parser.parse_args()

    session = SessionLocal()
    try:
        total = 0
        for uidx in range(1, args.users + 1):
            user = create_user(session, uidx)
            txs: list[Transaction] = []
            for _ in range(args.tx_per_user):
                cat = random.choice(DEFAULT_CATEGORIES)
                amt = random_amount(cat)
                tx = Transaction(date=random_date(args.days), description=f"Synthetic {cat}", amount=amt, category=cat, user_id=user.id)
                txs.append(tx)

            # add in chunks to avoid big transactions
            for i in range(0, len(txs), args.batch_size):
                chunk = txs[i : i + args.batch_size]
                session.add_all(chunk)
                session.commit()
                total += len(chunk)

        print(f"Inserted {total} transactions across {args.users} users.")
    finally:
        session.close()


if __name__ == "__main__":
    main()
