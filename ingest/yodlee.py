"""Simple Yodlee connector stub.

Yodlee has a more involved onboarding; this file is a placeholder to show
where integration would live. The function returns an empty list when no
credentials are provided.
"""
from __future__ import annotations

import os
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


def fetch_transactions(*args, **kwargs) -> List[Dict[str, Any]]:
    api_key = os.getenv("YODLEE_API_KEY")
    if not api_key:
        logger.info("Yodlee API key not set; returning empty list.")
        return []
    logger.info("Yodlee API key present but connector is a stub.")
    return []
