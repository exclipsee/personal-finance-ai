import csv
from db import insert_transaction


def import_csv(path: str, db_path: str = 'lite.db', date_col: str = 'date', desc_col: str = 'description', amount_col: str = 'amount') -> int:
    """Import transactions from a CSV file with header columns for date, description, amount.
    Returns number of rows imported."""
    count = 0
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            date = row.get(date_col, '')
            desc = row.get(desc_col, '')
            amt = row.get(amount_col, '0')
            try:
                amt = float(amt)
            except Exception:
                amt = 0.0
            insert_transaction(date, desc, amt, db_path=db_path)
            count += 1
    return count
