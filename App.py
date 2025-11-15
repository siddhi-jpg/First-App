import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Daily Expense Tracker", page_icon="💸", layout="centered")

# Styling
st.markdown("""
<style>
body {background-color: #f4f6f9;}
</style>
""", unsafe_allow_html=True)

st.title("💸 Daily Expense Tracker")

FILE = "expenses.csv"

# Load or create file
try:
    df = pd.read_csv(FILE)
except:
    df = pd.DataFrame(columns=["Date", "Category", "Amount", "Note"])
    df.to_csv(FILE, index=False)

# Add Expense
st.header("➕ Add Expense")

col1, col2 = st.columns(2)

with col1:
    amount = st.number_input("Amount (₹)", min_value=0.0, step=1.0)

with col2:
    category = st.selectbox(
        "Category",
        ["Food", "Transport", "Shopping", "Bills", "Entertainment", "Other"]
    )

note = st.text_input("Note (optional)")
date = st.date_input("Date", datetime.today())

if st.button("Add Expense"):
    new_entry = {"Date": date, "Category": category, "Amount": amount, "Note": note}
    df = df._append(new_entry, ignore_index=True)
    df.to_csv(FILE, index=False)
    st.success("Expense added!")

# Monthly Filter
st.header("📅 Filter by Month")

df["Date"] = pd.to_datetime(df["Date"])

months_available = df["Date"].dt.strftime("%Y-%m").unique()

if len(months_available) > 0:
    selected_month = st.selectbox("Select Month", sorted(months_available, reverse=True))
    filtered_df = df[df["Date"].dt.strftime("%Y-%m") == selected_month]
else:
    filtered_df = pd.DataFrame()

# Display Table
st.header("📊 Monthly Expenses")
st.dataframe(filtered_df, use_container_width=True)

# Summary
st.header("📈 Summary")

if not filtered_df.empty:
    total = filtered_df["Amount"].sum()
    st.metric("Total Spent This Month", f"₹{total:.2f}")

    category_summary = filtered_df.groupby("Category")["Amount"].sum().reset_index()

    # Pie chart
    fig = px.pie(
        category_summary,
        names="Category",
        values="Amount",
        title="Category-wise Spending",
        hole=0.4
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No data for this month.")
