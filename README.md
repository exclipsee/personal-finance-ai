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

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the app:**
   ```bash
   streamlit run app.py
   ```

3. **Start tracking:**
   - Import your transaction data (CSV format)
   - Or manually add transactions
   - Explore insights and predictions

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

This is a portfolio project, but contributions and suggestions are welcome!

## 📜 License

MIT License – free to use and modify.

