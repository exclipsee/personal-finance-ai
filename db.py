import sqlite3
from typing import List, Tuple


def init_db(db_path: str = 'lite.db') -> None:
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY,
        date TEXT,
        description TEXT,
        amount REAL,
        category TEXT
    )
    ''')
    conn.commit()
    conn.close()


def insert_transaction(date: str, description: str, amount: float, db_path: str = 'lite.db') -> None:
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('INSERT INTO transactions (date, description, amount, category) VALUES (?,?,?,NULL)'
              , (date, description, amount))
    conn.commit()
    conn.close()


def list_transactions(db_path: str = 'lite.db') -> List[Tuple]:
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT id, date, description, amount, category FROM transactions ORDER BY id DESC')
    rows = c.fetchall()
    conn.close()
    return rows


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
