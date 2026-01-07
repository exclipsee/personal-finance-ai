import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os
from pathlib import Path
import json


def _fmt_money(val):
    try:
        return f"${val:,.2f}"
    except Exception:
        return str(val)

st.set_page_config(
    page_title="Personal Finance AI Assistant",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title
st.title("💰 Personal Finance AI Assistant")
st.markdown("Analyze your spending, predict expenses, and get AI-powered financial insights")

# lightweight: no external logging/metrics in simplified app

# Initialize session state
if 'transactions' not in st.session_state:
    st.session_state.transactions = pd.DataFrame()
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'onboard_shown' not in st.session_state:
    st.session_state.onboard_shown = False
if 'theme' not in st.session_state:
    st.session_state.theme = 'System'

# Sidebar
with st.sidebar:
    # Theme selector
    st.markdown("**Appearance**")
    theme_choice = st.selectbox("Theme", options=["System", "Light", "Dark"], index=["System", "Light", "Dark"].index(st.session_state.get('theme', 'System')))
    st.session_state.theme = theme_choice
    if theme_choice == 'Dark':
        # Immediate CSS
        st.markdown(
            """
            <style>
            [data-testid="stAppViewContainer"] { background-color: #0e1117 !important; color: #e6eef8 !important; }
            .stApp .block-container { background-color: #0e1117 !important; color: #e6eef8 !important; }
            [data-testid="stSidebar"] { background-color: #0e1117 !important; color: #e6eef8 !important; }
            [data-testid="stToolbar"] { background-color: #0e1117 !important; color: #e6eef8 !important; }
            button[kind] { background-color: #1f2937 !important; color: #e6eef8 !important; }
            input, textarea { background-color: #0e1117 !important; color: #e6eef8 !important; }
            </style>
            """,
            unsafe_allow_html=True,
        )
        # Persist theme selection so Streamlit native theming applies after restart
        try:
            cfg_dir = Path('.streamlit')
            cfg_dir.mkdir(exist_ok=True)
            cfg_file = cfg_dir / 'config.toml'
            text = cfg_file.read_text(encoding='utf-8') if cfg_file.exists() else ''
            lines = []
            skip = False
            for line in text.splitlines():
                if line.strip().startswith('[theme]'):
                    skip = True
                    continue
                if skip and line.startswith('['):
                    skip = False
                if not skip:
                    lines.append(line)
            new_text = '\n'.join(lines).strip() + '\n\n[theme]\nbase = "dark"\n'
            cfg_file.write_text(new_text, encoding='utf-8')
            st.info('Theme persisted to .streamlit/config.toml — restart the app to apply to the entire UI.')
        except Exception as e:
            logger.exception('failed to persist theme', extra={'error': str(e)})
    else:
        # Remove any persisted theme section so Streamlit returns to system/default theme
        try:
            cfg_file = Path('.streamlit') / 'config.toml'
            if cfg_file.exists():
                text = cfg_file.read_text(encoding='utf-8')
                lines = []
                skip = False
                for line in text.splitlines():
                    if line.strip().startswith('[theme]'):
                        skip = True
                        continue
                    if skip and line.startswith('['):
                        skip = False
                    if not skip:
                        lines.append(line)
                cfg_file.write_text('\n'.join(lines).strip() + '\n', encoding='utf-8')
        except Exception:
            pass

    st.header("📊 Navigation")
    page = st.radio(
        "Choose a page",
        ["🏠 Dashboard", "📈 Analysis", "🤖 AI Insights", "🎯 Goals"]
    )
    
    st.divider()
    st.markdown("### Quick Stats")
    if not st.session_state.transactions.empty:
        total_expenses = st.session_state.transactions[st.session_state.transactions['amount'] < 0]['amount'].sum()
        total_income = st.session_state.transactions[st.session_state.transactions['amount'] > 0]['amount'].sum()
        st.metric("Total Expenses", _fmt_money(abs(total_expenses)))
        st.metric("Total Income", _fmt_money(total_income))
        st.metric("Net", _fmt_money(total_income + total_expenses))
    else:
        st.info("Import data to see stats")

# Main content based on selected page
if page == "🏠 Dashboard":
    st.header("Dashboard")
    
    if st.session_state.transactions.empty:
        st.info("Use the Import Data panel below to get started")
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
        # Onboarding panel
        if not st.session_state.onboard_shown:
            with st.expander("🧭 Quick Start / Onboarding", expanded=True):
                st.markdown("""
                **Welcome!** This short guide will help you get started:

                1. Import a CSV or use the sample data to explore quickly.
                2. Review recent transactions and categories on the Dashboard.
                3. Use the Analysis page to view trends and forecasts.
                4. Connect a bank feed later for automatic imports.
                """)
                col_a, col_b = st.columns([1,1])
                with col_a:
                    if st.button("Load sample data"):
                        sample_path = Path("data") / "sample_transactions.csv"
                        if sample_path.exists():
                            df = pd.read_csv(sample_path, parse_dates=['date'])
                        else:
                            df = pd.DataFrame([
                                { 'date': pd.to_datetime('2024-01-15'), 'description': 'Grocery Store', 'amount': -45.50, 'category': 'Food' },
                                { 'date': pd.to_datetime('2024-01-16'), 'description': 'Salary', 'amount': 3000.00, 'category': 'Income' },
                                { 'date': pd.to_datetime('2024-01-17'), 'description': 'Restaurant', 'amount': -28.00, 'category': 'Food' },
                            ])
                        st.session_state.transactions = df
                        st.session_state.data_loaded = True
                        st.success("Sample data loaded — explore the Dashboard!")
                with col_b:
                    if st.button("Dismiss onboarding"):
                        st.session_state.onboard_shown = True
                        st.experimental_rerun()
        # Embedded import UI
        with st.expander("📥 Import Data", expanded=True):
            tab1, tab2 = st.tabs(["📤 Upload CSV", "✏️ Manual Entry"])

            with tab1:
                st.markdown("### Upload CSV File")
                st.markdown("""
                Your CSV should have these columns:
                - `date` - Transaction date (DD/MM/YYYY)
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
                            try:
                                df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y', errors='coerce')
                                if df['date'].isna().any():
                                    df['date'] = pd.to_datetime(df['date'], dayfirst=True, errors='coerce')
                            except:
                                df['date'] = pd.to_datetime(df['date'], dayfirst=True, errors='coerce')

                            # Check for invalid dates and warn user
                            invalid_dates = df['date'].isna().sum()
                            if invalid_dates > 0:
                                st.warning(f"⚠️ {invalid_dates} row(s) have invalid dates and will be excluded from date-based analysis.")

                            # Ensure amount is numeric
                            df['amount'] = pd.to_numeric(df['amount'], errors='coerce')

                            # Auto-categorize if category missing
                            if 'category' not in df.columns:
                                df['category'] = 'Uncategorized'

                            st.session_state.transactions = df
                            st.session_state.data_loaded = True
                            st.success(f"✅ Loaded {len(df)} transactions!")
                            display_df = df.head().copy()
                            # Only format valid dates
                            display_df.loc[display_df['date'].notna(), 'date'] = display_df.loc[display_df['date'].notna(), 'date'].dt.strftime('%d/%m/%Y')
                            st.dataframe(display_df, use_container_width=True)

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
    else:
        # Display summary cards
        col1, col2, col3, col4 = st.columns(4)
        
        df = st.session_state.transactions
        expenses = df[df['amount'] < 0]
        income = df[df['amount'] > 0]
        
        with col1:
            st.metric("Total Transactions", len(df))
        with col2:
            total_exp_val = abs(expenses['amount'].sum())
            st.metric("Total Expenses", _fmt_money(total_exp_val))
        with col3:
            total_inc_val = income['amount'].sum()
            st.metric("Total Income", _fmt_money(total_inc_val))
        with col4:
            net = total_inc_val + ( - total_exp_val )
            # preserve delta behavior
            delta_pct = f"{(net/total_exp_val*100) if total_exp_val else 0:.1f}%"
            st.metric("Net Balance", _fmt_money(net), delta=delta_pct)
        
        # Recent transactions
        st.subheader("Recent Transactions")
        display_df = df.sort_values('date', ascending=False, na_position='last').head(10).copy()
        # Only format valid dates, leave NaT as is (will show as NaT in display)
        display_df.loc[display_df['date'].notna(), 'date'] = display_df.loc[display_df['date'].notna(), 'date'].dt.strftime('%d/%m/%Y')
        st.dataframe(
            display_df,
            use_container_width=True
        )

# Import UI has been embedded into the Dashboard; the separate Import page was removed.

elif page == "📈 Analysis":
    st.header("Spending Analysis")
    
    if st.session_state.transactions.empty:
        st.warning("No data loaded. Please import transactions first.")
    else:
        df = st.session_state.transactions.copy()
        # Filter out NaT (Not a Time) values for date operations
        valid_dates = df['date'].dropna()
        
        if valid_dates.empty:
            st.error("No valid dates found in the data. Please check your date format.")
        else:
            expenses = df[df['amount'] < 0].copy()
            expenses['amount'] = expenses['amount'].abs()
            
            # Time period selector - use valid dates only
            min_date = valid_dates.min().date() if not valid_dates.empty else datetime.now().date()
            max_date = valid_dates.max().date() if not valid_dates.empty else datetime.now().date()
            
            col1, col2 = st.columns(2)
            with col1:
                start_date = st.date_input("Start Date", value=min_date)
            with col2:
                end_date = st.date_input("End Date", value=max_date)
            
            # Filter by date range, excluding NaT values
            date_mask = df['date'].notna() & (df['date'].dt.date >= start_date) & (df['date'].dt.date <= end_date)
            filtered_df = df[date_mask]
            filtered_expenses = filtered_df[filtered_df['amount'] < 0].copy()
            filtered_expenses['amount'] = filtered_expenses['amount'].abs()
            
            # Charts — selectable, fancier options
            col1, col2 = st.columns(2)

            # --- Left: Spending by Category with chart selector ---
            with col1:
                st.subheader("Spending by Category")

                    if filtered_expenses.empty or 'category' not in filtered_expenses.columns:
                        st.info("No category data available")
                    else:
                        top_n = st.selectbox("Top categories to show", options=[5, 10, 20, 50], index=1)
                        category_sum = filtered_expenses.groupby('category')['amount'].sum().abs().sort_values(ascending=False).head(top_n)
                        st.subheader("Expenses by Category")
                        st.bar_chart(category_sum)

            # --- Right: Spending Over Time with frequency and chart selector ---
            with col2:
                st.subheader("Spending Over Time")

                if filtered_expenses.empty:
                    st.info("No spending data in selected date range")
                else:
                    # Prepare valid dated expenses
                    valid_expenses = filtered_expenses[filtered_expenses['date'].notna()].copy()
                        freq = st.selectbox("Frequency", options=["Daily", "Weekly", "Monthly"], index=0)
                        rule_map = {"Daily": 'D', "Weekly": 'W', "Monthly": 'M'}
                        rule = rule_map.get(freq, 'D')

                        valid_expenses['date'] = pd.to_datetime(valid_expenses['date'])
                        ts = valid_expenses.set_index('date').resample(rule)['amount'].sum().abs()

                        if ts.empty:
                            st.info("No time-series data after resampling")
                        else:
                            choice = st.selectbox("Chart type", options=["Line", "Bar", "Rolling Average", "Heatmap"], index=0)
                            if choice in ("Line", "Bar"):
                                st.line_chart(ts)
                            elif choice == "Rolling Average":
                                window_map = {'D':7, 'W':4, 'M':3}
                                w = window_map.get(rule, 7)
                                rolling = ts.rolling(window=w, min_periods=1).mean()
                                df_ts = pd.DataFrame({'amount': ts, 'rolling': rolling})
                                st.line_chart(df_ts)
                            else:
                                ve = valid_expenses.copy()
                                ve['month'] = ve['date'].dt.strftime('%Y-%m')
                                ve['weekday'] = ve['date'].dt.day_name()
                                pivot = ve.groupby(['month','weekday'])['amount'].sum().abs().reset_index()
                                weekdays = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
                                pivot['weekday'] = pd.Categorical(pivot['weekday'], categories=weekdays, ordered=True)
                                heat = pivot.pivot(index='weekday', columns='month', values='amount').fillna(0)
                                if heat.empty:
                                    st.info("Not enough data to build heatmap")
                                else:
                                    st.dataframe(heat)

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

