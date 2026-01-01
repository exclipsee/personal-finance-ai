# 💰 Personal Finance AI Assistant

An intelligent personal finance assistant that analyzes your spending, predicts future expenses, suggests budgets, detects anomalies, and provides actionable financial insights using machine learning.

## ✨ Features

- **Expense Tracking**: Import and categorize transactions from CSV, bank statements, or manual entry
- **Spending Analysis**: Visualize spending patterns by category, time period, and trends
- **Budget Recommendations**: AI-powered budget suggestions based on your spending patterns
- **Expense Prediction**: Predict future expenses using time series forecasting
- **Anomaly Detection**: Identify unusual spending patterns and potential fraud
- **Financial Insights**: Get personalized recommendations for saving and optimizing expenses
- **Goal Tracking**: Set and track financial goals (savings, debt payoff, etc.)
- **Interactive Dashboard**: Beautiful, intuitive interface built with Streamlit

## 🚀 Quick Start
1. Create and activate a Python virtual environment (recommended):

   - macOS / Linux:
     ```bash
     python -m venv .venv
     source .venv/bin/activate
     ```

   - Windows (PowerShell):
     ```powershell
     python -m venv .venv
     .\\.venv\\Scripts\\Activate.ps1
     ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the Streamlit app (default port 8501):

   ```bash
   streamlit run app.py
   ```

4. Start tracking:

   - Use the app UI to import a transaction CSV (see "Sample CSV" below).
   - Or add transactions manually via the dashboard.
   - Explore spending visualizations, budgets, and predictions.

## Usage Examples

- Run only the web UI on a different port:

  ```bash
  streamlit run app.py --server.port 8502
  ```

- Quick inspect of a CSV from the command line (preview first 5 rows):

  ```bash
  python -c "import pandas as pd; print(pd.read_csv('data/sample_transactions.csv').head())"
  ```

- Programmatic example (load CSV and show totals by category):

  ```python
  import pandas as pd

  df = pd.read_csv('data/sample_transactions.csv', parse_dates=['date'])
  totals = df.groupby('category')['amount'].sum()
  print(totals.sort_values())
  ```

## Sample CSV

Place a sample file at `data/sample_transactions.csv` (create the `data/` folder if missing). Example rows:

```csv
date,description,amount,category
2024-01-15,Grocery Store,-45.50,Food
2024-01-16,Salary,3000.00,Income
2024-01-17,Restaurant,-28.00,Food
```

Tip: the app accepts ISO dates (YYYY-MM-DD) and will auto-categorize missing `category` values where possible.

## 📊 Data Format

Your transaction CSV should have columns:
- `date` - Transaction date (DD/MM/YYYY)
- `description` - Transaction description
- `amount` - Amount (negative for expenses, positive for income)
- `category` - Category (optional, will be auto-categorized if missing)

Example:
```csv
date,description,amount,category
15/01/2024,Grocery Store,-45.50,Food
16/01/2024,Salary,3000.00,Income
17/01/2024,Restaurant,-28.00,Food
```

## 🧩 Tech Stack

- **Python 3.10+**
- **Streamlit** - Interactive web dashboard
- **Pandas** - Data manipulation and analysis
- **Scikit-learn** - Machine learning models
- **Prophet/FBProphet** - Time series forecasting
- **Plotly** - Interactive visualizations
- **SQLite** - Local data storage

## 📈 Roadmap

- [x] Project setup
- [ ] Transaction import and categorization
- [ ] Spending analysis dashboard
- [ ] Budget recommendation engine
- [ ] Expense prediction models
- [ ] Anomaly detection
- [ ] Financial goal tracking
- [ ] Export and reporting features
- [ ] Bank integration (API)

## 🤝 Contributing

This is a personal hobby project that I use to help manage my own finances. It reflects how I track and analyze spending for my personal use and is not financial advice. Contributions and suggestions are welcome, but please be mindful that this repository contains examples and utilities tailored to my personal workflows.

## 📜 License

MIT License – free to use and modify.

## Docker

Run the app locally with Docker (recommended for replicable environments):

Build the image:

```bash
docker build -t personal-finance-ai:latest .
```

Run with Docker:

```bash
docker run --rm -p 8501:8501 -v "${PWD}":/app personal-finance-ai:latest
```

Or use Docker Compose for development (hot-reloads via mounted volume):

```bash
docker compose up --build
```

Notes:
- The Docker image installs build tools to support packages that require compilation (e.g., some forecasting libs). The container exposes port `8501`.
- If you prefer a lightweight image for production, we can create a multi-stage Dockerfile to build wheels first and then copy them into a slimmer runtime image.

