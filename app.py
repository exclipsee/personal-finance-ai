"""
Personal Finance AI Assistant
Main Streamlit application
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from pathlib import Path
import json

# Page configuration
st.set_page_config(
    page_title="Personal Finance AI Assistant",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title
st.title("💰 Personal Finance AI Assistant")
st.markdown("Analyze your spending, predict expenses, and get AI-powered financial insights")

# Initialize session state
if 'transactions' not in st.session_state:
    st.session_state.transactions = pd.DataFrame()
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False

# Sidebar
with st.sidebar:
    st.header("📊 Navigation")
    page = st.radio(
        "Choose a page",
        ["🏠 Dashboard", "📥 Import Data", "📈 Analysis", "🤖 AI Insights", "🎯 Goals"]
    )
    
    st.divider()
    st.markdown("### Quick Stats")
    if not st.session_state.transactions.empty:
        total_expenses = st.session_state.transactions[st.session_state.transactions['amount'] < 0]['amount'].sum()
        total_income = st.session_state.transactions[st.session_state.transactions['amount'] > 0]['amount'].sum()
        st.metric("Total Expenses", f"${abs(total_expenses):,.2f}")
        st.metric("Total Income", f"${total_income:,.2f}")
        st.metric("Net", f"${total_income + total_expenses:,.2f}")
    else:
        st.info("Import data to see stats")

# Main content based on selected page
if page == "🏠 Dashboard":
    st.header("Dashboard")
    
    if st.session_state.transactions.empty:
        st.info("👈 Go to 'Import Data' to get started!")
        st.markdown("""
        ### Welcome to Personal Finance AI Assistant!
        
        This tool helps you:
        - 📊 Analyze your spending patterns
        - 🤖 Get AI-powered budget recommendations
        - 📈 Predict future expenses
        - 🔍 Detect unusual spending
        - 🎯 Track financial goals
        
        **Get started by importing your transaction data!**
        """)
    else:
        # Display summary cards
        col1, col2, col3, col4 = st.columns(4)
        
        df = st.session_state.transactions
        expenses = df[df['amount'] < 0]
        income = df[df['amount'] > 0]
        
        with col1:
            st.metric("Total Transactions", len(df))
        with col2:
            st.metric("Total Expenses", f"${abs(expenses['amount'].sum()):,.2f}")
        with col3:
            st.metric("Total Income", f"${income['amount'].sum():,.2f}")
        with col4:
            net = income['amount'].sum() + expenses['amount'].sum()
            st.metric("Net Balance", f"${net:,.2f}", delta=f"{net/abs(expenses['amount'].sum())*100:.1f}%")
        
        # Recent transactions
        st.subheader("Recent Transactions")
        st.dataframe(
            df.sort_values('date', ascending=False).head(10),
            use_container_width=True
        )

elif page == "📥 Import Data":
    st.header("Import Transaction Data")
    
    tab1, tab2 = st.tabs(["📤 Upload CSV", "✏️ Manual Entry"])
    
    with tab1:
        st.markdown("### Upload CSV File")
        st.markdown("""
        Your CSV should have these columns:
        - `date` - Transaction date (YYYY-MM-DD)
        - `description` - Transaction description
        - `amount` - Amount (negative for expenses, positive for income)
        - `category` - Category (optional)
        """)
        
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
        
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                
                # Validate required columns
                required_cols = ['date', 'description', 'amount']
                if not all(col in df.columns for col in required_cols):
                    st.error(f"Missing required columns. Need: {', '.join(required_cols)}")
                else:
                    # Convert date column
                    df['date'] = pd.to_datetime(df['date'])
                    
                    # Ensure amount is numeric
                    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
                    
                    # Auto-categorize if category missing
                    if 'category' not in df.columns:
                        df['category'] = 'Uncategorized'
                    
                    st.session_state.transactions = df
                    st.session_state.data_loaded = True
                    st.success(f"✅ Loaded {len(df)} transactions!")
                    st.dataframe(df.head(), use_container_width=True)
                    
            except Exception as e:
                st.error(f"Error loading file: {str(e)}")
    
    with tab2:
        st.markdown("### Add Transaction Manually")
        
        col1, col2 = st.columns(2)
        with col1:
            trans_date = st.date_input("Date", value=datetime.now())
            description = st.text_input("Description")
        with col2:
            amount = st.number_input("Amount", value=0.00, step=0.01)
            category = st.text_input("Category", value="Uncategorized")
        
        if st.button("Add Transaction"):
            new_trans = pd.DataFrame([{
                'date': trans_date,
                'description': description,
                'amount': amount,
                'category': category
            }])
            
            if st.session_state.transactions.empty:
                st.session_state.transactions = new_trans
            else:
                st.session_state.transactions = pd.concat([st.session_state.transactions, new_trans], ignore_index=True)
            
            st.success("Transaction added!")
            st.rerun()

elif page == "📈 Analysis":
    st.header("Spending Analysis")
    
    if st.session_state.transactions.empty:
        st.warning("No data loaded. Please import transactions first.")
    else:
        df = st.session_state.transactions
        expenses = df[df['amount'] < 0].copy()
        expenses['amount'] = expenses['amount'].abs()
        
        # Time period selector
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date", value=df['date'].min().date())
        with col2:
            end_date = st.date_input("End Date", value=df['date'].max().date())
        
        filtered_df = df[(df['date'].dt.date >= start_date) & (df['date'].dt.date <= end_date)]
        filtered_expenses = filtered_df[filtered_df['amount'] < 0].copy()
        filtered_expenses['amount'] = filtered_expenses['amount'].abs()
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Spending by Category")
            if not filtered_expenses.empty and 'category' in filtered_expenses.columns:
                category_sum = filtered_expenses.groupby('category')['amount'].sum().sort_values(ascending=False)
                fig = px.pie(
                    values=category_sum.values,
                    names=category_sum.index,
                    title="Expenses by Category"
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No category data available")
        
        with col2:
            st.subheader("Spending Over Time")
            if not filtered_expenses.empty:
                daily_spending = filtered_expenses.groupby(filtered_expenses['date'].dt.date)['amount'].sum()
                fig = px.line(
                    x=daily_spending.index,
                    y=daily_spending.values,
                    title="Daily Spending",
                    labels={'x': 'Date', 'y': 'Amount ($)'}
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # Category breakdown table
        st.subheader("Category Breakdown")
        if not filtered_expenses.empty and 'category' in filtered_expenses.columns:
            category_stats = filtered_expenses.groupby('category').agg({
                'amount': ['sum', 'mean', 'count']
            }).round(2)
            category_stats.columns = ['Total', 'Average', 'Count']
            category_stats = category_stats.sort_values('Total', ascending=False)
            st.dataframe(category_stats, use_container_width=True)

elif page == "🤖 AI Insights":
    st.header("AI-Powered Insights")
    
    if st.session_state.transactions.empty:
        st.warning("No data loaded. Please import transactions first.")
    else:
        st.info("🚧 AI features coming soon! This will include:")
        st.markdown("""
        - **Budget Recommendations**: AI-suggested budgets based on your spending patterns
        - **Expense Predictions**: Forecast future expenses using time series models
        - **Anomaly Detection**: Identify unusual spending patterns
        - **Savings Opportunities**: Personalized recommendations for saving money
        """)
        
        # Placeholder for future ML features
        df = st.session_state.transactions
        expenses = df[df['amount'] < 0]
        
        if not expenses.empty:
            st.subheader("Quick Insights")
            avg_daily = expenses['amount'].abs().sum() / (expenses['date'].max() - expenses['date'].min()).days
            st.metric("Average Daily Spending", f"${avg_daily:.2f}")

elif page == "🎯 Goals":
    st.header("Financial Goals")
    
    st.info("🚧 Goal tracking coming soon!")
    st.markdown("""
    Future features:
    - Set savings goals
    - Track debt payoff progress
    - Monitor spending limits
    - Get goal-based recommendations
    """)

