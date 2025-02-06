import streamlit as st
import pandas as pd
import plotly.express as px
from pyecharts import options as opts
from pyecharts.charts import Line
from streamlit_echarts import st_pyecharts

# Set Streamlit page layout
st.set_page_config(layout="wide")

# Title of the dashboard
st.title("Sugar Data Dashboard - NCDEX")

# Load data from Google Sheets (Modify URL accordingly)
csv_url = "Sugar Prices.xlsv"
df = pd.read_excel(csv_url)

# Ensure correct data types
df = df[["Date", "Kolhapur (S)"]].copy()
df["Date"] = pd.to_datetime(df["Date"], errors='coerce')  # Convert Date column to datetime format
df = df.dropna()  # Remove any rows with missing values
df = df.sort_values("Date")

# Convert "Kolhapur (S)" column to numeric
df["Kolhapur (S)"] = pd.to_numeric(df["Kolhapur (S)"], errors='coerce')

# Section Heading
st.subheader("Latest Trading Data")

# Metric Cards to display the latest row
latest_row = df.iloc[-1]
last_price_value = latest_row["Kolhapur (S)"]

# Extract previous day's data for comparison
previous_row = df.iloc[-2] if len(df) > 1 else latest_row
previous_price = previous_row["Kolhapur (S)"]
previous_date = previous_row["Date"]

# Calculate percentage change
percentage_change = round(((last_price_value - previous_price) / previous_price) * 100, 2)
delta_value = f"{percentage_change}%"

# Display Metrics
col1, col2 = st.columns(2)
col1.metric(label="Latest Price (Kolhapur)", value=f"{last_price_value:,.2f}", delta=delta_value, delta_color="inverse",border=True)
col2.metric(label="Previous Price", value=f"{previous_price:,.2f}",border=True)

# Trend Line Data
unique_dates_df = df.drop_duplicates(subset="Date", keep="first")
dates = unique_dates_df["Date"].dt.strftime("%Y-%m-%d").tolist()  # Convert dates to string format
prices = unique_dates_df["Kolhapur (S)"].tolist()

# Display Data Table
st.subheader("Data Table")
st.dataframe(df)

# Trend Line Chart
st.subheader("Price Trend Over Time")
chart = (
    Line()
    .add_xaxis(dates)
    .add_yaxis(
        "Kolhapur Price",
        prices,
        markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="max")]),
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="Past Price Trends"),
        yaxis_opts=opts.AxisOpts(interval=50, min_=min(prices)-10, max_=max(prices)+10),
    )
)

# Render the chart
st_pyecharts(chart, key="secharts")
