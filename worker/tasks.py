"""Celery tasks that wrap existing long-running scripts/functions."""
from __future__ import annotations

from pathlib import Path
import sys
import os
import logging

# Ensure project root is on path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from celery_app import celery_app

from db.database import SessionLocal

import ingest.csv_import as csv_import
import scripts.backup_db as backup_mod
import scripts.retention_purge as retention_mod

logger = logging.getLogger(__name__)


@celery_app.task(name="tasks.import_csv")
def import_csv_task(path: str, bank: str | None = None) -> dict:
    session_factory = SessionLocal
    inserted = csv_import.normalize_and_insert(path, session_factory, bank=bank)
    return {"inserted": inserted}


# Embeddings and categorization tasks have been offloaded; stubs remain
@celery_app.task(name="tasks.build_embeddings")
def build_embeddings_task(provider: str = "auto") -> dict:
    return {"error": "Embeddings functionality is offloaded. Re-enable by adding the extras package."}


@celery_app.task(name="tasks.train_categorizer")
def train_categorizer_task() -> dict:
    return {"error": "Categorization functionality is offloaded. Re-enable by adding the extras package."}


@celery_app.task(name="tasks.backup_db")
def backup_db_task() -> dict:
    db_path = Path(os.getenv("DATABASE_FILE", "./finance.db"))
    out_dir = Path(os.getenv("BACKUP_DIR", "backups"))
    key = os.getenv("DB_BACKUP_KEY")
    path = backup_mod.backup_db(db_path, out_dir, key)
    return {"backup": str(path)}


@celery_app.task(name="tasks.retention_purge")
def retention_purge_task() -> dict:
    days = int(os.getenv("RETENTION_DAYS", "365"))
    removed = retention_mod.purge_old_transactions(days)
    return {"removed": removed}
