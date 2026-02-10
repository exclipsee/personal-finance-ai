#!/usr/bin/env python
import argparse
import sys
import os
from pathlib import Path

# ensure repo root is importable when running the script
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from excel import export_xlsx
from db import get_all_transactions


def main():
    p = argparse.ArgumentParser(description='Export transactions')
    p.add_argument('--output', '-o', default='export.xlsx', help='Output file path (xlsx)')
    p.add_argument('--db', default='lite.db', help='SQLite DB path')
    args = p.parse_args()

    out = Path(args.output)
    export_xlsx(str(out), db_path=args.db)
    print(f'Wrote {out}')


if __name__ == '__main__':
    main()
