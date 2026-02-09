KEYWORD_CATEGORIES = {
    'Coffee': ['starbucks', 'coffee', 'cafe', 'espresso'],
    'Groceries': ['walmart', 'whole foods', 'safeway', 'grocery', 'supermarket', 'aldi', 'trader joe'],
    'Transport': ['uber', 'lyft', 'taxi', 'metro', 'bus', 'train', 'uber eats'],
    'Rent': ['rent', 'landlord'],
    'Income': ['salary', 'payroll', 'deposit', 'paycheck'],
    'Utilities': ['electric', 'water', 'gas', 'utility', 'internet']
}


def categorize_transaction(description: str, amount: float) -> str:
    s = (description or '').lower()
    for category, keywords in KEYWORD_CATEGORIES.items():
        for k in keywords:
            if k in s:
                return category
    # Use amount heuristics: positive amounts probably income
    if amount and amount > 0:
        return 'Income'
    return 'Uncategorized'


def categorize_all(db_path: str = 'lite.db') -> int:
    from db import fetch_uncategorized, update_category
    rows = fetch_uncategorized(db_path=db_path)
    updated = 0
    for r in rows:
        tx_id, date, desc, amount = r
        cat = categorize_transaction(desc, amount)
        update_category(tx_id, cat, db_path=db_path)
        updated += 1
    return updated
