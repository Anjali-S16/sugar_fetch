import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.charts import Line
from streamlit_echarts import st_pyecharts
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


# Drop duplicate dates and keep the first occurrence of each date
unique_dates_df = df.drop_duplicates(subset='Price Date', keep='first')

# Extract lists of dates and prices
dates = unique_dates_df['Price Date'].tolist()  # Format as string
prices = unique_dates_df['Price'].tolist()
print(dates,prices,"&&&")
# Output the lists
print("Dates:", dates)
print("Prices:", prices)
col1, col2 = st.columns(2)

# Table in the first column
with col1:
    st.dataframe(df)

# Trend Line in the second column
with col2:
    
    c = (
    Line()
    .add_xaxis(dates)
    .add_yaxis(
        "Price",
        prices,
        markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="max")]),
    )
    .set_global_opts(
            title_opts=opts.TitleOpts(title="Price Trend with MarkPoint"),
            yaxis_opts=opts.AxisOpts(
                interval=30, 
                  min_=3400,    # Set the minimum value of the y-axis
            max_=3600,  # Set the interval to 50 for y-axis ticks
            ),
        )
    )
   
   
                      
    
    
    st_pyecharts(c, key="secharts") 
