"""
Utility functions for Personal Finance AI Assistant
"""
import pandas as pd
from datetime import datetime
from typing import Dict, List, Optional
import re

def load_transactions(file_path: str) -> pd.DataFrame:
    """Load transactions from CSV file."""
    df = pd.read_csv(file_path)
    df['date'] = pd.to_datetime(df['date'])
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
    return df

def auto_categorize(description: str, categories: Optional[Dict[str, List[str]]] = None) -> str:
    """
    Auto-categorize transaction based on description.
    
    Args:
        description: Transaction description
        categories: Optional custom category keywords
    
    Returns:
        Category name
    """
    if categories is None:
        categories = {
            'Food': ['grocery', 'restaurant', 'coffee', 'food', 'mcdonald', 'starbucks', 'pizza'],
            'Transportation': ['gas', 'uber', 'lyft', 'taxi', 'parking', 'metro', 'bus'],
            'Entertainment': ['netflix', 'spotify', 'movie', 'cinema', 'concert', 'game'],
            'Shopping': ['amazon', 'target', 'walmart', 'store', 'purchase'],
            'Health': ['pharmacy', 'doctor', 'hospital', 'medicine', 'cvs', 'walgreens'],
            'Bills': ['electric', 'water', 'internet', 'phone', 'utility', 'bill'],
            'Income': ['salary', 'paycheck', 'deposit', 'refund'],
        }
    
    desc_lower = description.lower()
    
    for category, keywords in categories.items():
        if any(keyword in desc_lower for keyword in keywords):
            return category
    
    return 'Other'

def calculate_summary_stats(df: pd.DataFrame) -> Dict:
    """Calculate summary statistics from transactions."""
    expenses = df[df['amount'] < 0]
    income = df[df['amount'] > 0]
    
    return {
        'total_transactions': len(df),
        'total_expenses': abs(expenses['amount'].sum()),
        'total_income': income['amount'].sum(),
        'net_balance': income['amount'].sum() + expenses['amount'].sum(),
        'avg_expense': abs(expenses['amount'].mean()) if not expenses.empty else 0,
        'avg_income': income['amount'].mean() if not income.empty else 0,
        'num_expenses': len(expenses),
        'num_income': len(income),
    }

def get_category_breakdown(df: pd.DataFrame) -> pd.DataFrame:
    """Get spending breakdown by category."""
    expenses = df[df['amount'] < 0].copy()
    expenses['amount'] = expenses['amount'].abs()
    
    if 'category' not in expenses.columns:
        return pd.DataFrame()
    
    breakdown = expenses.groupby('category').agg({
        'amount': ['sum', 'mean', 'count']
    }).round(2)
    breakdown.columns = ['Total', 'Average', 'Count']
    breakdown = breakdown.sort_values('Total', ascending=False)
    
    return breakdown

def get_daily_spending(df: pd.DataFrame) -> pd.Series:
    """Get daily spending totals."""
    expenses = df[df['amount'] < 0].copy()
    expenses['amount'] = expenses['amount'].abs()
    
    if expenses.empty:
        return pd.Series(dtype=float)
    
    daily = expenses.groupby(expenses['date'].dt.date)['amount'].sum()
    return daily

def filter_by_date_range(df: pd.DataFrame, start_date: datetime, end_date: datetime) -> pd.DataFrame:
    """Filter transactions by date range."""
    return df[(df['date'].dt.date >= start_date.date()) & (df['date'].dt.date <= end_date.date())]

