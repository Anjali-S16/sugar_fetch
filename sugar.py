import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
st.set_page_config(layout="wide")
# Title of the dashboard
st.title("Sugar Data Dashboard")

# Sample data
# Replace this with your actual dataset

df = pd.read_excel("SpotPricesDetails.xlsx")

# Sort data by date for a proper trend line

df = df.sort_values("Price Date")
df["Price Date"] = df["Price Date"].astype(str)

df["Price Time"] = df["Price Time"].astype(str)

print(df.dtypes)
# Section heading
st.subheader("Latest Trading Data")

# Metric Cards to display the latest row
latest_row = df.iloc[-1]
cols = st.columns(len(latest_row) - 1)  # Exclude the "Date" column from metrics
for i, col in enumerate(latest_row.index[1:]):
    cols[i].metric(label=col, value=latest_row[col])

# Layout: Table and Trend Line
st.subheader("Trading Data and Trends")
col1, col2 = st.columns(2)

# Table in the first column
with col1:
    st.dataframe(df)

# Trend Line in the second column
with col2:
    trend_fig = px.line(df, x="Price Date", y="Price", title="Closing Price Trend")
    st.plotly_chart(trend_fig, use_container_width=True)
