"""Utility helpers for Personal Finance AI Assistant"""
import pandas as pd
from datetime import datetime
from typing import Dict, List, Optional
import re
import math

def _to_float(v):
    try:
        return float(v)
    except Exception:
        return 0.0

def load_transactions(file_path: str) -> pd.DataFrame:
    """Load transactions from CSV file."""
    df = pd.read_csv(file_path)
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
    if 'amount' in df.columns:
        df['amount'] = df['amount'].apply(_to_float)
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
    
    desc_lower = (description or '').lower()

    for category, keywords in categories.items():
        for kw in keywords:
            if kw in desc_lower:
                return category

    return 'Other'

def calculate_summary_stats(df: pd.DataFrame) -> Dict:
    """Calculate summary statistics from transactions."""
    expenses = df[df['amount'] < 0]
    income = df[df['amount'] > 0]
    
    total_exp = expenses['amount'].sum() if not expenses.empty else 0
    total_inc = income['amount'].sum() if not income.empty else 0
    avg_exp = abs(expenses['amount'].mean()) if not expenses.empty else 0
    avg_inc = income['amount'].mean() if not income.empty else 0

    return {
        'total_transactions': len(df),
        'total_expenses': abs(total_exp),
        'total_income': total_inc,
        'net_balance': total_inc + total_exp,
        'avg_expense': avg_exp,
        'avg_income': avg_inc,
        'num_expenses': len(expenses),
        'num_income': len(income),
    }

def get_category_breakdown(df: pd.DataFrame) -> pd.DataFrame:
    """Get spending breakdown by category."""
    expenses = df[df['amount'] < 0].copy()
    expenses['amount'] = expenses['amount'].abs()
    
    if 'category' not in expenses.columns:
        return pd.DataFrame()
    
    grouped = expenses.groupby('category').agg({
        'amount': ['sum', 'mean', 'count']
    }).round(2)
    grouped.columns = ['Total', 'Average', 'Count']
    return grouped.sort_values('Total', ascending=False)

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
    mask = (df['date'].dt.date >= start_date.date()) & (df['date'].dt.date <= end_date.date())
    return df[mask]

