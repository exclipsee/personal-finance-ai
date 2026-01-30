# Agent

Small AI agent helpers for `personal-finance-ai`.

Usage
- Summarize transactions (reads local DB via `db/database.py`):

```bash
python run_agent.py summarize --limit 200
```

- Fetch Kaggle metadata (optional; requires local Kaggle configuration):

```bash
export KAGGLE_API_TOKEN=your_token_here
python run_agent.py fetch-kaggle --query "personal finance" --max 5
```

Security
- Never commit API tokens or `kaggle.json` to the repository. Use environment
  variables or local configuration files excluded via `.gitignore`.
- This project reads `OPENAI_API_KEY` and `KAGGLE_API_TOKEN` from the
  environment if present and will gracefully fall back when they are not.

Local development with a `.env` file
- Create a `.env` file at the project root to store development-only secrets.
  Example `.env`:

```dotenv
# .env (do not commit)
OPENAI_API_KEY=sk_...       # optional
KAGGLE_API_TOKEN=KGAT_...   # optional
DATABASE_URL=sqlite:///./finance.db
```

- The `run_agent.py` command will automatically load `./.env` if present.
- Add `.env` to `.gitignore` to avoid accidental commits (see project README).

CSV import and connectors
- Use `scripts/import_csv.py` to import bank CSV exports into the local DB.

```powershell
python scripts/import_csv.py path/to/your.csv --bank chase
```

- There are stubs for Plaid and Yodlee in `ingest/plaid.py` and `ingest/yodlee.py`.
  Real integration requires installing the provider SDKs and setting credentials
  in environment variables (see `.env.example`).

Categorization ML
- Categorization & embeddings have been moved to an optional extras package to keep this repository lightweight. If you need the full ML tooling, extract the `ingest/` ML modules into a separate package and install the extra dependencies (`scikit-learn`, `joblib`, `numpy`).
- The feedback CLI remains available: `python scripts/feedback_cli.py --tx 123 --new "Groceries" --user demo`.

Privacy & Compliance
- Export a user's data (transactions + feedback) for portability:

```powershell
python scripts/export_user.py --username demo --out exports/demo.json
```

- Delete a user's data (destructive; requires `--yes`):

```powershell
python scripts/delete_user.py --username demo --yes
```

- Purge old data according to retention policy (reads `RETENTION_DAYS` from env):

```powershell
python scripts/retention_purge.py
```

- Create an encrypted backup of the local DB (requires `DB_BACKUP_KEY` in env):

```powershell
# generate key (do NOT commit)
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
$env:DB_BACKUP_KEY = '...'
python scripts/backup_db.py
```
