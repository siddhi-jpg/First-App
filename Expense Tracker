import streamlit as st
import pandas as pd
from datetime import datetime

st.title("💰 Daily Expense Tracker")

# Initialize CSV
FILE = "expenses.csv"

# Create file if it doesn't exist
try:
    df = pd.read_csv(FILE)
except:
    df = pd.DataFrame(columns=["Date", "Category", "Amount", "Note"])
    df.to_csv(FILE, index=False)

st.subheader("➕ Add New Expense")

# Inputs
amount = st.number_input("Amount (₹)", min_value=0.0, step=1.0)
category = st.selectbox("Category", ["Food", "Transport", "Shopping", "Bills", "Other"])
note = st.text_input("Note (optional)")
date = st.date_input("Date", datetime.today())

# Save button
if st.button("Add Expense"):
    new_data = {"Date": date, "Category": category, "Amount": amount, "Note": note}
    df = df._append(new_data, ignore_index=True)
    df.to_csv(FILE, index=False)
    st.success("Expense added successfully!")

st.subheader("📊 All Expenses")
st.dataframe(df)

# Summary
st.subheader("📈 Summary")

if not df.empty:
    total = df["Amount"].sum()
    st.write(f"### Total Spent: ₹{total}")

    category_summary = df.groupby("Category")["Amount"].sum()

    st.bar_chart(category_summary)
else:
    st.info("No expenses added yet.")
