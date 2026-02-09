import tempfile
import pandas as pd
from typing import Dict, Any

import db
from excel import import_xlsx


def merge_xlsx(path: str, db_path: str = 'lite.db') -> Dict[str, Any]:
    """Merge an uploaded XLSX into the DB.
    Merge rules:
    - If `external_id` column present and matches existing transaction -> update that transaction.
    - Else try exact date+amount match -> update.
    - Else try partial description+amount fuzzy match -> update.
    - Else insert as new transaction.

    Returns a summary dict.
    """
    db.init_db(db_path)
    df = pd.read_excel(path, sheet_name=None, engine='openpyxl')
    if isinstance(df, dict):
        df = list(df.values())[0]
    # normalize columns
    df.columns = [c.strip().lower() for c in df.columns]
    results = {
        'inserted': 0,
        'updated': 0,
        'matched_by_external_id': 0,
        'matched_by_date_amount': 0,
        'matched_by_fuzzy': 0,
        'errors': []
    }
    for _, row in df.iterrows():
        try:
            external_id = row.get('external_id') if 'external_id' in df.columns else None
            date = row.get('date', '')
            desc = row.get('description', '')
            amount = row.get('amount', 0)
            category = row.get('category') if 'category' in df.columns else None
            # normalize amount
            try:
                amount = float(amount)
            except Exception:
                amount = 0.0
            tx_id = None
            if external_id and not pd.isna(external_id):
                tx_id = db.find_by_external_id(str(external_id), db_path=db_path)
                if tx_id:
                    db.update_transaction(tx_id, date, desc, amount, category=category, external_id=str(external_id), db_path=db_path)
                    results['updated'] += 1
                    results['matched_by_external_id'] += 1
                    continue
            # try date+amount
            tx_id = db.find_by_date_amount_description(date, amount, desc, db_path=db_path)
            if tx_id:
                db.update_transaction(tx_id, date, desc, amount, category=category, external_id=(str(external_id) if external_id and not pd.isna(external_id) else None), db_path=db_path)
                results['updated'] += 1
                results['matched_by_date_amount'] += 1
                continue
            # insert new
            db.insert_transaction(date, desc, amount, db_path=db_path, external_id=(str(external_id) if external_id and not pd.isna(external_id) else None), category=category)
            results['inserted'] += 1
        except Exception as e:
            results['errors'].append(str(e))
    return results
