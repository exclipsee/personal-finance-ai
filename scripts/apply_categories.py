#!/usr/bin/env python
import argparse
import sys
import os
# ensure repo root is importable when running the script
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from excel import apply_category_updates


def main():
    p = argparse.ArgumentParser(description='Apply category edits from an XLSX file to the DB')
    p.add_argument('file', help='Path to XLSX file to read')
    p.add_argument('--db', default='lite.db', help='SQLite DB path')
    args = p.parse_args()

    updated = apply_category_updates(args.file, db_path=args.db)
    print(f'Updated {updated} transactions')


if __name__ == '__main__':
    main()
