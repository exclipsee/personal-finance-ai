
Personal Finance AI - Lite

This is a compact, Excel-friendly subset of the original project. It focuses on quick CSV/XLSX import/export, simple categorization rules, and a tiny sync API so you can edit transactions in Excel and push changes back.

Quick start (Windows PowerShell):

python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python test_smoke.py          # quick local smoke test (creates lite.db)

Excel workflows (recommended):
- Use `templates/transaction_template.xlsx` as an import template.
- Export current transactions (XLSX):
	- GET /sync/pull?format=xlsx  -> downloads `transactions.xlsx`
- Edit categories in Excel (edit the `category` column or add `external_id`).
- Re-upload edited file to merge changes:
	- POST /sync/upload (multipart form file field `file`) -> returns a merge summary

API endpoints (important):
- POST /init       : initialize the SQLite DB
- POST /import     : import CSV (multipart `file`)
- GET  /transactions : list transactions (JSON)
- POST /categorize : run rule-based categorizer
- GET  /sync/pull  : return all transactions (JSON) or XLSX when `?format=xlsx`
- POST /sync/upload: accept XLSX and merge into DB (matches by `external_id` or date+amount/description)

Files and helpers:
- `excel.py`            : XLSX import/export and apply-category helper
- `sync.py`             : merge logic for XLSX uploads (simple rules)
- `templates/transaction_template.xlsx` : example import template
- `examples/roundtrip_example.xlsx`     : sample exported file to edit and re-upload

Example curl commands:

curl -X POST http://127.0.0.1:5000/init

curl -F "file=@transactions.xlsx" http://127.0.0.1:5000/sync/upload

curl http://127.0.0.1:5000/sync/pull?format=xlsx --output transactions.xlsx

Notes and next steps:
- Editable roundtrip: export XLSX, edit `category`, re-upload to apply edits.
- For live Excel integration consider `xlwings` (optional, included in `requirements.txt`).
- Add tests/CI and a small web UI for bulk editing if you want to scale this beyond a single-user local tool.

If you'd like, I can add short CLI scripts (`scripts/export.py` and `scripts/apply_categories.py`) or update this README with screenshots and a short video workflow.
CLI & Web UI

Quick CLI examples (run from repo root):

Windows PowerShell

python scripts\export.py --output transactions.xlsx
python scripts\apply_categories.py transactions_edited.xlsx

Run the web UI (starts Flask server and open http://127.0.0.1:5000/ui):

python app.py

The UI shows a simple editable table and uses these endpoints:
- GET /api/transactions  -> returns JSON list of transactions
- POST /api/apply_bulk   -> accepts {updates: [{id, category}]} to apply edits

Recommended next steps: add auth for the UI, pagination, or an "Export" button that downloads XLSX directly from the page.

