Personal Finance AI - Lite

This is a minimal, runnable subset of the original project. It supports:
- SQLite storage for transactions
- CSV import (headers: date, description, amount)
- Simple rule-based categorizer
- Small Flask API with endpoints: /init, /import, /transactions, /categorize

Quick start (Windows PowerShell):

python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m personal_finance_ai_lite.app

Endpoints:
- POST /init -> initialize the DB
- POST /import (multipart form file field `file`) -> import CSV
- GET /transactions -> list transactions
- POST /categorize -> run categorizer on uncategorized transactions
