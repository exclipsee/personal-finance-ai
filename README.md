# Personal Finance AI

A compact, Excel-friendly personal finance helper. Import transactions from CSV or XLSX, do quick automatic categorization using keyword rules, export to XLSX for round-trip editing, and sync edits back into the local SQLite DB.

This repository aims to be minimal and easy to use locally. It includes a tiny Flask web UI for bulk edits, simple categorization rules, and small utilities for import/export and syncing with Excel.

## Features

- Import transactions from CSV/XLSX
- Export transactions to XLSX for Excel round-trip editing
- Simple keyword-based auto-categorization
- Tiny sync API for exporting/importing XLSX edits
- Lightweight SQLite (`lite.db`) as the data store
- New: `/balance` endpoint that returns the sum of all transaction amounts

## Quickstart

1. Clone the repository

   ```bash
   git clone https://github.com/your-username/personal-finance-ai.git
   cd personal-finance-ai
   ```

2. Create and activate a Python virtual environment (recommended)

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies

   ```bash
   python3 -m pip install -r requirements.txt
   ```

4. Initialize the database (or let the app create it on first run)

   You can initialize the DB using the web API or by calling the helper directly. To initialize via API:

   ```bash
   # start the app (next step) then:
   curl -X POST http://127.0.0.1:5000/init
   ```

   Or from Python:

   ```python
   from db import init_db
   init_db('lite.db')
   ```

5. Run the web app

   ```bash
   python app.py
   ```

   Open the UI at: http://127.0.0.1:5000/ui

## API Endpoints

- `GET /transactions` — list recent transactions (JSON)
- `GET /api/transactions` — list all transactions (JSON, includes `external_id`)
- `POST /import` — upload a CSV file to import transactions (multipart form, field `file`)
- `POST /categorize` — run automatic categorization on uncategorized transactions
- `GET /sync/pull` — export transactions as JSON (or `?format=xlsx` to download an XLSX)
- `POST /sync/upload` — upload an XLSX exported from `sync/pull` to merge edits back (multipart form, field `file`)
- `POST /api/apply_bulk` — apply a JSON set of category updates (body `{"updates": [{"id": 1, "category": "Groceries"}, ...]}`)
- `GET /balance` — returns JSON `{ "balance": <float> }` where `balance` is the sum of all `amount` values in the DB

## Command-line utilities / scripts

- `scripts/apply_categories.py <file.xlsx>` — apply category edits from an XLSX file back to the DB
- `scripts/create_templates.py` and `scripts/export.py` — small helpers for templating/exporting (see file headers)

## Contributing

Contributions and suggestions welcome. Open an issue or submit a pull request. For larger changes, please open an issue first so we can discuss the design.
