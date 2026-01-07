# Personal Finance AI Assistant

Small Streamlit app to import and analyze personal transaction CSVs, visualize spending, and experiment with ML features. This repo includes a simplified Streamlit UI and lightweight build options to make local runs quick.

Quick start
-----------
- Create and activate a virtual environment (optional but recommended):

  ```bash
  python -m venv .venv
  # macOS / Linux
  source .venv/bin/activate
  # Windows (PowerShell)
  .\.venv\Scripts\Activate.ps1
  ```

- Install full dependencies and run the (original/full) app:

  ```bash
  pip install -r requirements.txt
  streamlit run app.py
  ```

Simplified (minimal) runtime
----------------------------
If you want a lightweight runtime (smaller install, faster container builds) use the minimal requirements and the slim Dockerfile added to the repo.

Install the minimal Python deps and run locally:

```bash
pip install -r requirements.minimal.txt
streamlit run app.py
```

Build and run the slim Docker image (uses `Dockerfile.slim`):

```bash
docker build -f Dockerfile.slim -t personal-finance-ai:slim .
docker run --rm -p 8501:8501 personal-finance-ai:slim
```

Sample CSV
----------
Place `data/sample_transactions.csv` containing at least these columns: `date,description,amount,category`.

Docker Compose (full stack)
---------------------------
There is a `docker-compose.yml` for running Postgres, Prometheus and Grafana alongside the app. Use `docker compose up` to start services if you need the full stack.

Notes
-----
- `app.py` has been simplified to use Streamlit-native charts (no Plotly) and to avoid external observability/logging in the simplified run.
- Use `requirements.txt` for the full feature set; use `requirements.minimal.txt` for a lighter install.

Contributing & License
----------------------
Contributions welcome; please open issues or PRs. Licensed under MIT.

