"""Robust CSV importer with fuzzy header matching and bank templates.

Features:
- Auto-detect common column names (date, description, amount, category)
- Fuzzy header matching using difflib
- Date parsing via dateutil if available, fallback to common formats
- Simple bank templates for mapping known CSV exports
"""
from __future__ import annotations

import csv
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
import difflib
import logging
from typing import Dict, Iterable, List, Optional

try:
    from dateutil import parser as dateutil_parser
except Exception:
    dateutil_parser = None  # type: ignore

logger = logging.getLogger(__name__)


COMMON_COLUMNS = ["date", "description", "amount", "category", "memo"]

BANK_TEMPLATES: Dict[str, Dict[str, str]] = {
    # Example mappings: header -> normalized column
    "chase": {"post date": "date", "description": "description", "amount": "amount", "type": "category"},
    "bankofamerica": {"date": "date", "description": "description", "amount": "amount"},
    "venmo": {"date": "date", "note": "description", "amount": "amount"},
}


@dataclass
class Row:
    date: Optional[datetime]
    description: str
    amount: float
    category: Optional[str]


def _fuzzy_map(headers: List[str], target: str) -> Optional[str]:
    """Return the header name that best matches the target column, or None."""
    matches = difflib.get_close_matches(target, headers, n=1, cutoff=0.6)
    return matches[0] if matches else None


def _parse_date(value: str) -> Optional[datetime]:
    if not value:
        return None
    value = value.strip()
    if dateutil_parser:
        try:
            return dateutil_parser.parse(value).date()
        except Exception:
            pass

    # fallback list of common formats
    fmts = ["%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y", "%m-%d-%Y"]
    for f in fmts:
        try:
            return datetime.strptime(value, f).date()
        except Exception:
            continue
    logger.debug("Unrecognized date format: %s", value)
    return None


def _parse_amount(value: str) -> Optional[float]:
    if value is None:
        return None
    v = value.strip().replace(",", "")
    try:
        return float(v)
    except Exception:
        # try to handle parentheses for negative values
        try:
            if v.startswith("(") and v.endswith(")"):
                return -float(v.strip("()"))
        except Exception:
            pass
    logger.debug("Unrecognized amount format: %s", value)
    return None


def detect_mapping(headers: Iterable[str], bank: Optional[str] = None) -> Dict[str, str]:
    """Return a mapping from normalized column names to CSV headers.

    If `bank` is supplied and present in `BANK_TEMPLATES`, prefer that mapping.
    """
    headers = [h.lower().strip() for h in headers]
    mapping: Dict[str, str] = {}

    if bank:
        tpl = BANK_TEMPLATES.get(bank.lower())
        if tpl:
            for h, norm in tpl.items():
                if h in headers:
                    mapping[norm] = h

    for target in COMMON_COLUMNS:
        if target in mapping:
            continue
        found = _fuzzy_map(headers, target)
        if found:
            mapping[target] = found

    return mapping


def read_csv(path: str, bank: Optional[str] = None) -> List[Row]:
    """Read CSV and return normalized rows.

    The function tolerates missing columns and logs skipped rows.
    """
    rows: List[Row] = []
    with open(path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        headers = list(reader.fieldnames or [])
        mapping = detect_mapping(headers, bank=bank)

        for i, raw in enumerate(reader, start=1):
            date_val = None
            if "date" in mapping:
                date_val = _parse_date(raw.get(mapping["date"], ""))
            description = raw.get(mapping.get("description", ""), "").strip()
            amount = None
            if "amount" in mapping:
                amount = _parse_amount(raw.get(mapping["amount"], ""))
            category = raw.get(mapping.get("category", ""), None)

            if amount is None:
                logger.debug("Skipping row %d due to missing amount: %s", i, raw)
                continue

            row = Row(date=date_val, description=description, amount=amount, category=category)
            rows.append(row)

    return rows


def normalize_and_insert(path: str, db_session_factory, bank: Optional[str] = None) -> int:
    """Read CSV at `path`, normalize and insert into DB via `db_session_factory` (callable producing sessions).

    Returns number of rows inserted.
    """
    session = db_session_factory()
    try:
        from db.models import Transaction

        parsed = read_csv(path, bank=bank)
        for r in parsed:
            tx = Transaction(date=r.date, description=r.description, amount=r.amount, category=(r.category or None))
            session.add(tx)
        session.commit()
        return len(parsed)
    finally:
        session.close()
