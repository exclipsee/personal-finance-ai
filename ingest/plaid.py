"""Simple Plaid connector stub.

This module provides a small wrapper function `fetch_transactions` which is
implemented as a stub here. To enable real Plaid integration, set the
`PLAID_CLIENT_ID` and `PLAID_SECRET` in the environment and install the
`plaid` SDK. For safety we do not ship real credentials or call Plaid in CI.
"""
from __future__ import annotations

import os
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


def fetch_transactions(start_date: str = None, end_date: str = None) -> List[Dict[str, Any]]:
    """Stub: return empty list or raise helpful error if creds missing."""
    client_id = os.getenv("PLAID_CLIENT_ID")
    secret = os.getenv("PLAID_SECRET")
    if not client_id or not secret:
        logger.info("Plaid credentials not configured; returning empty list.")
        return []

    # Real implementation would create a Plaid client and fetch transactions.
    logger.info("Plaid credentials configured but the connector is a stub in this repo.")
    return []
