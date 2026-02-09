import pandas as pd
from typing import Optional

from db import insert_transaction, list_transactions, update_category, init_db


def import_xlsx(path: str, db_path: str = 'lite.db', sheet_name: Optional[str] = None,
                date_col: str = 'date', desc_col: str = 'description', amount_col: str = 'amount') -> int:
    """Read an XLSX file and insert rows into the DB. Columns can be configured by name.
    Returns number of rows imported."""
    # ensure DB schema exists
    init_db(db_path)
    df = pd.read_excel(path, sheet_name=sheet_name, engine='openpyxl')
    # If multiple sheets were returned (sheet_name=None) pick the first
    if isinstance(df, dict):
        # take the first sheet
        df = list(df.values())[0]
    # Normalize column names to lower for flexible matching
    df.columns = [c.strip().lower() for c in df.columns]
    date_c = date_col.lower()
    desc_c = desc_col.lower()
    amount_c = amount_col.lower()
    count = 0
    for _, row in df.iterrows():
        date = row.get(date_c, '')
        desc = row.get(desc_c, '')
        amt = row.get(amount_c, 0)
        try:
            amt = float(amt)
        except Exception:
            amt = 0.0
        insert_transaction(date, desc, amt, db_path=db_path)
        count += 1
    return count


def export_xlsx(path: str, db_path: str = 'lite.db', sheet_name: str = 'Transactions') -> None:
    """Export transactions from the DB to an XLSX file."""
    rows = list_transactions(db_path=db_path)
    # rows: list of tuples (id, date, description, amount, category)
    df = pd.DataFrame(rows, columns=['id', 'date', 'description', 'amount', 'category'])
    # Write to excel
    df.to_excel(path, index=False, sheet_name=sheet_name, engine='openpyxl')


def apply_category_updates(path: str, db_path: str = 'lite.db', sheet_name: Optional[str] = None) -> int:
    """Read an XLSX file and apply category edits back to the DB.
    If the sheet contains an `id` column, it will be used to match and update the `category` field.
    Returns number of updated rows."""
    df = pd.read_excel(path, sheet_name=sheet_name, engine='openpyxl')
    if isinstance(df, dict):
        df = list(df.values())[0]
    df.columns = [c.strip().lower() for c in df.columns]
    updated = 0
    if 'id' in df.columns and 'category' in df.columns:
        for _, row in df.iterrows():
            try:
                tx_id = int(row.get('id'))
            except Exception:
                continue
            cat = row.get('category')
            if pd.isna(cat):
                continue
            update_category(tx_id, str(cat), db_path=db_path)
            updated += 1
    return updated
