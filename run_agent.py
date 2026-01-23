"""Small CLI runner for the `agent` helpers."""
from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path

from dotenv import load_dotenv

from agent.agent import summarize_transactions, fetch_kaggle_metadata

logging.basicConfig(level=logging.INFO)

# Load local .env automatically if present for developer convenience.
env_path = Path(__file__).parent / ".env"
if env_path.exists():
    load_dotenv(env_path)


def main() -> None:
    parser = argparse.ArgumentParser(prog="run_agent.py", description="Run small AI helpers for personal-finance-ai")
    sub = parser.add_subparsers(dest="cmd")

    p_sum = sub.add_parser("summarize", help="Summarize recent transactions")
    p_sum.add_argument("--limit", type=int, default=100, help="Number of recent transactions to include")

    p_kag = sub.add_parser("fetch-kaggle", help="Fetch Kaggle metadata (optional)")
    p_kag.add_argument("--query", type=str, default="", help="Search query for Kaggle datasets")
    p_kag.add_argument("--max", type=int, default=5, help="Maximum results to return")

    args = parser.parse_args()

    if args.cmd == "summarize":
        result = summarize_transactions(limit=args.limit)
        print(json.dumps(result, indent=2, default=str))
    elif args.cmd == "fetch-kaggle":
        result = fetch_kaggle_metadata(query=args.query, max_results=args.max)
        print(json.dumps(result, indent=2, default=str))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
