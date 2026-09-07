import streamlit as st
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "transformed"

st.title("TransactionPulse Dashboard")

# 1. LOAD DATA FIRST
customer_summary = pd.read_csv(DATA_PATH / "customer_summary.csv")
merchant_summary = pd.read_csv(DATA_PATH / "merchant_summary.csv")
transactions_full = pd.read_csv(DATA_PATH / "transactions_full.csv")

st.write("Data loaded successfully!")
st.write(f"Customers: {len(customer_summary)}, Merchants: {len(merchant_summary)}, Transactions: {len(transactions_full)}")

# 2. THEN metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Customers", len(customer_summary))
col2.metric("Total Merchants", len(merchant_summary))
col3.metric("Total Revenue", f"₹{merchant_summary['total_revenue'].sum():,.0f}")

# 3. THEN the sidebar filter (now customer_summary already exists)
st.sidebar.header("Filters")
selected_type = st.sidebar.selectbox("Customer Type", ["All"] + list(customer_summary["customer_type"].unique()))

if selected_type != "All":
    filtered_customers = customer_summary[customer_summary["customer_type"] == selected_type]
else:
    filtered_customers = customer_summary

# 4. THEN your charts (merchants, customers, table) — using filtered_customers where noted

customer_summary = pd.read_csv(DATA_PATH / "customer_summary.csv")
merchant_summary = pd.read_csv(DATA_PATH / "merchant_summary.csv")
transactions_full = pd.read_csv(DATA_PATH / "transactions_full.csv")

st.header("Top 10 Customers by Spending")

top_customers = filtered_customers.sort_values("total_spent", ascending=False).head(10)

st.bar_chart(top_customers.set_index("customer_name")["total_spent"])

st.header("Top 10 Customers by Spending")

top_customers = customer_summary.sort_values("total_spent", ascending=False).head(10)

st.bar_chart(top_customers.set_index("customer_name")["total_spent"])

st.header("All Transactions")

st.dataframe(transactions_full)

st.header("Transactions Needing Review")

needs_review = pd.read_csv(PROJECT_ROOT / "data" / "clean" / "transactions_needs_review.csv")

st.write(f"{len(needs_review)} transactions were flagged during cleaning (negative amounts or future dates) instead of being deleted.")
st.dataframe(needs_review)