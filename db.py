import sqlite3
from typing import List, Tuple, Optional


def init_db(db_path: str = 'lite.db') -> None:
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY,
        date TEXT,
        description TEXT,
        amount REAL,
        category TEXT,
        external_id TEXT
    )
    ''')
    # ensure external_id column exists for older DBs
    c.execute("PRAGMA table_info(transactions)")
    cols = [r[1] for r in c.fetchall()]
    if 'external_id' not in cols:
        try:
            c.execute('ALTER TABLE transactions ADD COLUMN external_id TEXT')
        except Exception:
            pass
    conn.commit()
    conn.close()


def insert_transaction(date: str, description: str, amount: float, db_path: str = 'lite.db', external_id: str = None, category: str = None) -> int:
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('INSERT INTO transactions (date, description, amount, category, external_id) VALUES (?,?,?,?,?)'
              , (date, description, amount, category, external_id))
    tx_id = c.lastrowid
    conn.commit()
    conn.close()
    return tx_id


def update_transaction(tx_id: int, date: str, description: str, amount: float, category: str = None, external_id: str = None, db_path: str = 'lite.db') -> None:
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('UPDATE transactions SET date=?, description=?, amount=?, category=?, external_id=? WHERE id=?',
              (date, description, amount, category, external_id, tx_id))
    conn.commit()
    conn.close()


def list_transactions(db_path: str = 'lite.db') -> List[Tuple]:
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT id, date, description, amount, category FROM transactions ORDER BY id DESC')
    rows = c.fetchall()
    conn.close()
    return rows


def get_all_transactions(db_path: str = 'lite.db') -> List[Tuple]:
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    try:
        c.execute('SELECT id, date, description, amount, category, external_id FROM transactions ORDER BY id')
        rows = c.fetchall()
    except Exception:
        # fallback if external_id column does not exist
        c.execute('SELECT id, date, description, amount, category FROM transactions ORDER BY id')
        rows = [(r[0], r[1], r[2], r[3], r[4], None) for r in c.fetchall()]
    conn.close()
    return rows


def find_by_external_id(external_id: str, db_path: str = 'lite.db') -> Optional[int]:
    if not external_id:
        return None
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT id FROM transactions WHERE external_id = ? LIMIT 1', (external_id,))
    r = c.fetchone()
    conn.close()
    return r[0] if r else None


def find_by_date_amount_description(date: str, amount: float, description: str, db_path: str = 'lite.db') -> Optional[int]:
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    # Try exact date+amount match first
    c.execute('SELECT id FROM transactions WHERE date = ? AND amount = ? LIMIT 1', (date, amount))
    r = c.fetchone()
    if r:
        conn.close()
        return r[0]
    # Fallback: try partial description match with amount
    if description:
        snippet = (description or '')[:20].lower()
        c.execute('SELECT id FROM transactions WHERE lower(description) LIKE ? AND amount = ? LIMIT 1', (f'%{snippet}%', amount))
        r = c.fetchone()
        conn.close()
        return r[0] if r else None
    conn.close()
    return None


def update_category(tx_id: int, category: str, db_path: str = 'lite.db') -> None:
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('UPDATE transactions SET category=? WHERE id=?', (category, tx_id))
    conn.commit()
    conn.close()


def fetch_uncategorized(db_path: str = 'lite.db') -> List[Tuple]:
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT id, date, description, amount FROM transactions WHERE category IS NULL OR category=''")
    rows = c.fetchall()
    conn.close()
    return rows


def get_balance(db_path: str = 'lite.db') -> float:
    """Return the sum of all transaction amounts as a float. Returns 0.0 for empty DB."""
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    try:
        c.execute('SELECT COALESCE(SUM(amount), 0) FROM transactions')
        r = c.fetchone()
        total = float(r[0]) if r and r[0] is not None else 0.0
    except Exception:
        total = 0.0
    conn.close()
    return total
