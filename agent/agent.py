"""Small AI agent helpers for the personal-finance-ai project.

This module provides simple functions to summarize transactions from the
local database and a helper to query Kaggle if a token and the `kaggle`
package are available. All external API keys are read from environment
variables and never written to disk by this code.
"""
from __future__ import annotations

import os
import logging
import json
from collections import Counter
from typing import Any, Dict, List

from db.database import SessionLocal
from db.models import Transaction

logger = logging.getLogger(__name__)


def summarize_transactions(limit: int = 100) -> Dict[str, Any]:
    """Return a small summary of the most recent transactions.

    If `OPENAI_API_KEY` is set the function will attempt an optional
    AI-generated natural-language summary. Failures to call external
    services are ignored and only included in logs.
    """
    session = SessionLocal()
    try:
        txs = (
            session.query(Transaction)
            .order_by(Transaction.date.desc())
            .limit(limit)
            .all()
        )
    finally:
        session.close()

    total = sum((t.amount or 0) for t in txs)
    count = len(txs)
    avg = total / count if count else 0.0
    categories = Counter((t.category or "Uncategorized") for t in txs)
    top_categories = categories.most_common(5)

    summary: Dict[str, Any] = {
        "count": count,
        "total": total,
        "average": avg,
        "top_categories": top_categories,
    }

    # Optional: produce a natural-language summary using OpenAI if configured.
    if os.getenv("OPENAI_API_KEY"):
        try:
            import openai

            openai.api_key = os.getenv("OPENAI_API_KEY")
            simple_list = [
                {"date": str(t.date), "description": (t.description or ""), "amount": t.amount, "category": (t.category or "")}
                for t in txs
            ]
            prompt = f"Summarize these transactions for a user in 3 short bullet points:\n{json.dumps(simple_list, default=str)}"
            resp = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful financial assistant."},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=300,
            )
            summary_text = resp["choices"][0]["message"]["content"].strip()
            summary["ai_summary"] = summary_text
        except Exception as e:  # pragma: no cover - optional integration
            logger.debug("OpenAI call failed: %s", e)

    return summary


def fetch_kaggle_metadata(query: str = "", max_results: int = 5) -> Dict[str, Any]:
    """Attempt to fetch metadata from Kaggle.

    This function does not print or store user tokens. It requires that
    the user configure the Kaggle environment (either via `kaggle` package
    authentication or their local `~/.kaggle/kaggle.json`). If no token is
    present the function will return a helpful message.
    """
    token = os.getenv("KAGGLE_API_TOKEN")
    if not token:
        return {"error": "KAGGLE_API_TOKEN not set in environment. Set it locally; do not commit secrets."}

    try:
        # Try to use the official Kaggle API if installed.
        from kaggle.api.kaggle_api_extended import KaggleApi

        api = KaggleApi()
        try:
            api.authenticate()
        except Exception:
            # Authentication commonly requires a kaggle.json or env vars
            # If it fails, return a helpful message without leaking the token.
            return {"error": "Failed to authenticate Kaggle API. Ensure your local kaggle configuration is correct."}

        results = api.dataset_list(search=query or None, page=1, page_size=max_results)
        items: List[Dict[str, Any]] = []
        for r in results:
            items.append({"ref": getattr(r, "ref", None), "title": getattr(r, "title", None)})

        return {"count": len(items), "items": items}
    except Exception as e:  # pragma: no cover - optional integration
        logger.debug("Kaggle query failed: %s", e)
        return {"message": "Kaggle token present but the `kaggle` package is not available/configured.", "error": str(e)}
