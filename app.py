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
        display_df = df.sort_values('date', ascending=False, na_position='last').head(10).copy()
        # Only format valid dates, leave NaT as is (will show as NaT in display)
        display_df.loc[display_df['date'].notna(), 'date'] = display_df.loc[display_df['date'].notna(), 'date'].dt.strftime('%d/%m/%Y')
        st.dataframe(
            display_df,
            use_container_width=True
        )

elif page == "📥 Import Data":
    st.header("Import Transaction Data")
    
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
                    # Convert date column - try European format first (DD/MM/YYYY), then fallback to auto-detect
                    try:
                        df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y', errors='coerce')
                        # If parsing failed, try other common formats
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
                    cat_choice = st.selectbox("Chart type", options=["Pie", "Donut", "Bar", "Treemap", "Sunburst"], index=1)

                    category_sum = filtered_expenses.groupby('category')['amount'].sum().sort_values(ascending=False)
                    category_sum = category_sum.head(top_n)

                    if cat_choice == "Pie":
                        fig = px.pie(values=category_sum.values, names=category_sum.index, title="Expenses by Category")
                        st.plotly_chart(fig, use_container_width=True)

                    elif cat_choice == "Donut":
                        fig = px.pie(values=category_sum.values, names=category_sum.index, title="Expenses by Category (Donut)", hole=0.4)
                        st.plotly_chart(fig, use_container_width=True)

                    elif cat_choice == "Bar":
                        fig = px.bar(x=category_sum.index, y=category_sum.values, title="Expenses by Category", labels={'x': 'Category', 'y': 'Amount ($)'})
                        fig.update_layout(xaxis={'categoryorder':'total descending'})
                        st.plotly_chart(fig, use_container_width=True)

                    elif cat_choice == "Treemap":
                        fig = px.treemap(names=category_sum.index, values=category_sum.values, title="Expenses Treemap")
                        st.plotly_chart(fig, use_container_width=True)

                    elif cat_choice == "Sunburst":
                        # Simple one-level sunburst (can be extended to hierarchical categories)
                        fig = px.sunburst(names=category_sum.index, values=category_sum.values, title="Expenses Sunburst")
                        st.plotly_chart(fig, use_container_width=True)

            # --- Right: Spending Over Time with frequency and chart selector ---
            with col2:
                st.subheader("Spending Over Time")

                if filtered_expenses.empty:
                    st.info("No spending data in selected date range")
                else:
                    # Prepare valid dated expenses
                    valid_expenses = filtered_expenses[filtered_expenses['date'].notna()].copy()
                    if valid_expenses.empty:
                        st.info("No valid dates in filtered data")
                    else:
                        freq = st.selectbox("Frequency", options=["Daily", "Weekly", "Monthly"], index=0)
                        time_chart = st.selectbox("Chart type", options=["Line", "Area", "Bar", "Rolling Average", "Heatmap (month vs weekday)"], index=0)

                        # Resample rule map
                        rule_map = {"Daily": 'D', "Weekly": 'W', "Monthly": 'M'}
                        rule = rule_map.get(freq, 'D')

                        # Ensure datetime index for resampling
                        valid_expenses['date'] = pd.to_datetime(valid_expenses['date'])
                        ts = valid_expenses.set_index('date').resample(rule)['amount'].sum().abs()

                        if ts.empty:
                            st.info("No time-series data after resampling")
                        else:
                            if time_chart in ("Line", "Area"):
                                title = f"{freq} Spending"
                                if time_chart == "Line":
                                    fig = px.line(x=ts.index, y=ts.values, title=title, labels={'x':'Date','y':'Amount ($)'})
                                else:
                                    fig = px.area(x=ts.index, y=ts.values, title=title, labels={'x':'Date','y':'Amount ($)'})
                                st.plotly_chart(fig, use_container_width=True)

                            elif time_chart == "Bar":
                                fig = px.bar(x=ts.index, y=ts.values, title=f"{freq} Spending (Bar)", labels={'x':'Date','y':'Amount ($)'})
                                st.plotly_chart(fig, use_container_width=True)

                            elif time_chart == "Rolling Average":
                                # Rolling window depends on frequency
                                window_map = {'D':7, 'W':4, 'M':3}
                                w = window_map.get(rule, 7)
                                rolling = ts.rolling(window=w, min_periods=1).mean()
                                fig = go.Figure()
                                fig.add_trace(go.Bar(x=ts.index, y=ts.values, name='Amount', marker_color='lightgray'))
                                fig.add_trace(go.Line(x=rolling.index, y=rolling.values, name=f'Rolling Avg ({w})', line=dict(color='crimson', width=3)))
                                fig.update_layout(title=f"{freq} Spending with Rolling Average")
                                st.plotly_chart(fig, use_container_width=True)

                            else:
                                # Heatmap: month vs weekday
                                ve = valid_expenses.copy()
                                ve['month'] = ve['date'].dt.strftime('%Y-%m')
                                ve['weekday'] = ve['date'].dt.day_name()
                                pivot = ve.groupby(['month','weekday'])['amount'].sum().abs().reset_index()
                                # Ensure weekdays order
                                weekdays = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
                                pivot['weekday'] = pd.Categorical(pivot['weekday'], categories=weekdays, ordered=True)
                                heat = pivot.pivot(index='weekday', columns='month', values='amount').fillna(0)
                                if heat.empty:
                                    st.info("Not enough data to build heatmap")
                                else:
                                    fig = go.Figure(data=go.Heatmap(
                                        z=heat.values,
                                        x=list(heat.columns),
                                        y=list(heat.index),
                                        colorscale='YlOrRd'
                                    ))
                                    fig.update_layout(title='Spending Heatmap (month vs weekday)', xaxis_title='Month', yaxis_title='Weekday')
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

