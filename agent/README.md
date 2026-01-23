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
