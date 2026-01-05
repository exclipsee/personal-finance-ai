# Personal Finance AI Assistant

Small Streamlit app to import and analyze personal transaction CSVs, visualize spending, and experiment with ML features. The project itself is rather a hobby, so everyone can copy it and control finances easily.

Quick start
---------
- Create and activate a virtual environment (optional but recommended):

  ```bash
  python -m venv .venv
  source .venv/bin/activate    # macOS / Linux
  .\.venv\Scripts\Activate.ps1  # Windows (PowerShell)
  ```

- Install dependencies and run the app:

  ```bash
  pip install -r requirements.txt
  streamlit run app.py
  ```

Sample CSV
---------
Place `data/sample_transactions.csv` containing at least these columns: `date,description,amount,category`.

Docker
------
Build and run:

```bash
docker build -t personal-finance-ai:latest .
docker run --rm -p 8501:8501 -v "${PWD}":/app personal-finance-ai:latest
```

Notes
-----
- The app accepts common date formats and will default missing categories to `Uncategorized`.
- This repo is a personal project; use at your own risk. See `requirements.txt` for dependency versions.

Contributing & License
----------------------
Contributions welcome; please open issues or PRs. Licensed under MIT.

