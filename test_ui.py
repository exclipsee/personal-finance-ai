from app import app

client = app.test_client()

# fetch transactions
resp = client.get('/api/transactions')
print('Transactions status:', resp.status_code)
rows = resp.get_json() or []
print('Count:', len(rows))
if rows:
    # modify first transaction's category
    first = rows[0]
    updates = [{'id': first['id'], 'category': (first.get('category') or '') + ' (edited)'}]
    rv = client.post('/api/apply_bulk', json={'updates': updates})
    print('Apply status:', rv.status_code, rv.get_json())
else:
    print('No transactions to edit')
