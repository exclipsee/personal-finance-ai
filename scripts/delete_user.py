"""Delete a user and optionally their associated transactions and feedback.

Usage: python scripts/delete_user.py --username demo --yes
This action is destructive; the script requires `--yes` to proceed.
"""
from __future__ import annotations

from pathlib import Path
import sys
import argparse

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from db.database import SessionLocal
from db.models import User, Transaction, CategoryFeedback


def delete_user(username: str) -> None:
    session = SessionLocal()
    try:
        user = session.query(User).filter_by(username=username).first()
        if not user:
            print(f"User not found: {username}")
            return

        # delete feedback and transactions associated with this user
        session.query(CategoryFeedback).filter_by(user_id=user.id).delete()
        session.query(Transaction).filter_by(user_id=user.id).delete()
        session.delete(user)
        session.commit()
        print(f"Deleted user and related data for {username}")
    finally:
        session.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--username", required=True)
    parser.add_argument("--yes", action="store_true", help="Confirm destructive action")
    args = parser.parse_args()
    if not args.yes:
        print("This will delete user data. Re-run with --yes to confirm.")
        return
    delete_user(args.username)


if __name__ == "__main__":
    main()
