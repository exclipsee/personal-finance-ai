"""Purge transactions older than a retention period.

Reads `RETENTION_DAYS` from environment (defaults to 365). Use carefully.
"""
from __future__ import annotations

from pathlib import Path
import os
import sys
from datetime import date, timedelta

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from db.database import SessionLocal
from db.models import Transaction


def purge_old_transactions(retention_days: int) -> int:
    session = SessionLocal()
    try:
        cutoff = date.today() - timedelta(days=retention_days)
        q = session.query(Transaction).filter(Transaction.date != None).filter(Transaction.date < cutoff)
        count = q.count()
        q.delete(synchronize_session=False)
        session.commit()
        return count
    finally:
        session.close()


def main():
    retention = int(os.getenv("RETENTION_DAYS", "365"))
    removed = purge_old_transactions(retention)
    print(f"Purged {removed} transactions older than {retention} days")


if __name__ == "__main__":
    main()
