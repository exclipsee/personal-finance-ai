from db import init_db, insert_transaction, list_transactions
from categorizer import categorize_all

DB_PATH = 'lite.db'

if __name__ == '__main__':
    print('Initializing DB...')
    init_db(DB_PATH)
    print('Inserting sample transactions...')
    insert_transaction('2026-02-01', 'Starbucks Coffee', -4.5, db_path=DB_PATH)
    insert_transaction('2026-02-02', 'ACME Payroll Deposit', 2500.0, db_path=DB_PATH)
    insert_transaction('2026-02-03', 'Walmart Supercenter', -76.23, db_path=DB_PATH)
    print('Running categorizer...')
    updated = categorize_all(db_path=DB_PATH)
    print(f'Categorizer updated {updated} transactions')
    print('Listing transactions:')
    for tx in list_transactions(DB_PATH):
        print(tx)
