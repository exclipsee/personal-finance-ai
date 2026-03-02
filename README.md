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
