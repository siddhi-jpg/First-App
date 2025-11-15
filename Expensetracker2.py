import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px

# --------------------- PAGE CONFIG ---------------------
st.set_page_config(
    page_title="Daily Expense Tracker",
    page_icon="💸",
    layout="centered",
)

# --------------------- STYLING ---------------------
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .title {
        color: #2c3e50;
        text-align: center;
        font-size: 40px !important;
        font-weight: 700;
        padding-bottom: 10px;
    }
    .subtitle {
        color: #34495e;
        font-size: 24px !important;
        font-weight: 600;
        padding-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --------------------- TITLE ---------------------
st.markdown("<h1 class='title'>💸 Daily Expense Tracker</h1>", unsafe_allow_html=True)

FILE = "expenses.csv"

# --------------------- LOAD/CREATE CSV ---------------------
try:
    df = pd.read_csv(FILE)
except:
    df = pd.DataFrame(columns=["Date", "Category", "Amount", "Note"])
    df.to_csv(FILE, index=False)

# --------------------- ADD EXPENSE SECTION ---------------------
st.markdown("<h2 class='subtitle'>➕ Add Expense</h2>", unsafe_allow_html=True)

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
    new_data = {"Date": date, "Category": category, "Amount": amount, "Note": note}
    df = df._append(new_data, ignore_index=True)
    df.to_csv(FILE, index=False)
    st.success("Expense added successfully!")

# --------------------- MONTHLY FILTER ---------------------
st.markdown("<h2 class='subtitle'>📅 Monthly Filter</h2>", unsafe_allow_html=True)

df["Date"] = pd.to_datetime(df["Date"])

all_months = df["Date"].dt.strftime("%Y-%m").unique()
selected_month = st.selectbox("Select Month", sorted(all_months, reverse=True))

# Filter data
filtered_df = df[df["Date"].dt.strftime("%Y-%m") == selected_month]

# --------------------- SHOW TABLE ---------------------
st.markdown("<h2 class='subtitle'>📊 Expense Table</h2>", unsafe_allow_html=True)

if filtered_df.empty:
    st.info("No expenses found for this month.")
else:
    st.dataframe(filtered_df.reset_index(drop=True), use_container_width=True)

# --------------------- SUMMARY ---------------------
st.markdown("<h2 class='subtitle'>📈 Summary</h2>", unsafe_allow_html=True)

if not filtered_df.empty:
    total = filtered_df["Amount"].sum()
    st.metric("Total Spent This Month", f"₹{total:,.2f}")

    # Category wise summary
    category_summary = filtered_df.groupby("Category")["Amount"].sum().reset_index()

    # --------------------- PIE CHART ---------------------
    fig_pie = px.pie(
        category_summary,
        names="Category",
        values="Amount",
        title="Category-wise Spending",
        hole=0.4
    )
    st.plotly_chart(fig_pie, use_container_width=True)

else:
    st.info("Add expenses to view summary.")

