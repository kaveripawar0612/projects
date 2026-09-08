import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Sales Performance Dashboard", page_icon="📊", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("data/sales_data.csv", parse_dates=["Date"])

df = load_data()

st.title("📊 Sales Performance Dashboard")
st.caption("Interactive portfolio dashboard using synthetic sample data")

with st.sidebar:
    st.header("Filters")
    regions = st.multiselect("Region", sorted(df["Region"].unique()), default=sorted(df["Region"].unique()))
    categories = st.multiselect("Category", sorted(df["Category"].unique()), default=sorted(df["Category"].unique()))
    date_range = st.date_input("Date range", [df["Date"].min().date(), df["Date"].max().date()])

filtered = df[df["Region"].isin(regions) & df["Category"].isin(categories)].copy()
if len(date_range) == 2:
    filtered = filtered[filtered["Date"].dt.date.between(date_range[0], date_range[1])]

revenue = filtered["Revenue"].sum()
profit = filtered["Profit"].sum()
orders = filtered["Order_ID"].nunique()
aov = revenue / orders if orders else 0

c1, c2, c3, c4 = st.columns(4)
c1.metric("Revenue", f"₹{revenue:,.0f}")
c2.metric("Profit", f"₹{profit:,.0f}")
c3.metric("Orders", f"{orders:,}")
c4.metric("Average Order Value", f"₹{aov:,.0f}")

monthly = filtered.assign(Month=filtered["Date"].dt.to_period("M").astype(str)).groupby("Month", as_index=False)[["Revenue", "Profit"]].sum()
regional = filtered.groupby("Region", as_index=False)[["Revenue", "Profit"]].sum().sort_values("Revenue", ascending=False)
category = filtered.groupby("Category", as_index=False)[["Revenue", "Profit"]].sum().sort_values("Revenue", ascending=False)

left, right = st.columns(2)
with left:
    st.subheader("Monthly Trend")
    st.plotly_chart(px.line(monthly, x="Month", y=["Revenue", "Profit"], markers=True), use_container_width=True)
with right:
    st.subheader("Regional Performance")
    st.plotly_chart(px.bar(regional, x="Region", y="Revenue", text_auto=".2s"), use_container_width=True)

left, right = st.columns(2)
with left:
    st.subheader("Category Performance")
    st.plotly_chart(px.bar(category, x="Category", y=["Revenue", "Profit"], barmode="group"), use_container_width=True)
with right:
    st.subheader("Top Products")
    products = filtered.groupby("Product", as_index=False)[["Revenue", "Profit"]].sum().sort_values("Revenue", ascending=False).head(10)
    st.dataframe(products, use_container_width=True, hide_index=True)

st.subheader("Filtered Sales Data")
st.dataframe(filtered.sort_values("Date", ascending=False), use_container_width=True, hide_index=True)
