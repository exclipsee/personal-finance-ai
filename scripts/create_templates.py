from openpyxl import Workbook
import os

os.makedirs('templates', exist_ok=True)
os.makedirs('examples', exist_ok=True)

# Create a simple transaction template
wb = Workbook()
ws = wb.active
ws.title = 'Transactions'
ws.append(['date', 'description', 'amount', 'external_id', 'category'])
# Example row for guidance
ws.append(['2026-02-01', 'Starbucks Coffee', -4.5, 'txn-001', 'Coffee'])
wb.save('templates/transaction_template.xlsx')

# Create a roundtrip example (export + edited categories)
wb2 = Workbook()
ws2 = wb2.active
ws2.title = 'Transactions'
ws2.append(['id', 'date', 'description', 'amount', 'category', 'external_id'])
ws2.append([1, '2026-02-01', 'Starbucks Coffee', -4.5, 'Coffee', 'txn-001'])
ws2.append([2, '2026-02-02', 'ACME Payroll Deposit', 2500.0, 'Income', 'txn-002'])
wb2.save('examples/roundtrip_example.xlsx')

print('Created templates/transaction_template.xlsx and examples/roundtrip_example.xlsx')