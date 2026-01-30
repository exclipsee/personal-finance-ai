"""Simple CLI to enqueue Celery tasks for common operations.

Example:
  python scripts/enqueue_task.py import_csv path/to/file.csv --bank chase
  python scripts/enqueue_task.py build_embeddings --provider tfidf
"""
from __future__ import annotations

from pathlib import Path
import sys
import argparse

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from worker.tasks import import_csv_task, build_embeddings_task, train_categorizer_task, backup_db_task, retention_purge_task


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd")

    p_imp = sub.add_parser("import_csv")
    p_imp.add_argument("path")
    p_imp.add_argument("--bank", default=None)

    p_be = sub.add_parser("build_embeddings")
    p_be.add_argument("--provider", default="auto")

    sub.add_parser("train_categorizer")
    sub.add_parser("backup_db")
    sub.add_parser("retention_purge")

    args = parser.parse_args()
    if args.cmd == "import_csv":
        res = import_csv_task.delay(args.path, args.bank)
        print(f"Enqueued import_csv task id={res.id}")
    elif args.cmd == "build_embeddings":
        res = build_embeddings_task.delay(args.provider)
        print(f"Enqueued build_embeddings task id={res.id}")
    elif args.cmd == "train_categorizer":
        res = train_categorizer_task.delay()
        print(f"Enqueued train_categorizer task id={res.id}")
    elif args.cmd == "backup_db":
        res = backup_db_task.delay()
        print(f"Enqueued backup_db task id={res.id}")
    elif args.cmd == "retention_purge":
        res = retention_purge_task.delay()
        print(f"Enqueued retention_purge task id={res.id}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
