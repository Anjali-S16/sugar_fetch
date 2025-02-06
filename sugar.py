import streamlit as st
import pandas as pd
import plotly.express as px

# Set Streamlit page layout
st.set_page_config(page_title="Sugar Data Dashboard", layout="wide")

# Path to the Hector Beverages logo (Since it's in 'photos' folder)
logo_path = "photos/hector_logo.png"  # Ensure the file is correctly named

# Custom CSS for Professional Dark Theme
st.markdown("""
    <style>
        /* Dark Mode Background */
        .main {
            background: #121212;
            color: white;
        }

        /* Title Styling */
        h1 {
            color: #ffa500; 
            text-align: center;
            font-size: 42px;
            font-weight: bold;
            font-family: 'Arial', sans-serif;
        }

        /* Metric Card Styling */
        div[data-testid="metric-container"] {
            background-color: #1e1e1e;
            border-radius: 10px;
            padding: 20px;
            border: 1px solid #ffa500;
            box-shadow: 2px 2px 10px rgba(255,165,0,0.2);
            text-align: center;
        }

        /* Bold Styling for Metric Labels */
        div[data-testid="stMetric"] > label {
            font-weight: bold;
            font-size: 18px;
            color: #ffa500; 
        }
        div[data-testid="stMetric"] > div {
            font-weight: bold;
            font-size: 22px;
        }

        /* Table Styling */
        .dataframe {
            background-color: #1e1e1e;
            color: white;
            border-radius: 10px;
            text-align: center;
            border: 1px solid #ffa500;
        }

        /* Chart Background */
        .stPlotlyChart {
            background-color: #1e1e1e;
            border-radius: 10px;
            padding: 15px;
        }
    </style>
""", unsafe_allow_html=True)

# Display Logo and Title
col1, col2 = st.columns([0.2, 0.8])  # Adjust column widths
with col1:
    st.image(logo_path, width=100)  # Adjust size as needed
with col2:
    st.markdown("<h1 style='color:#ffa500; font-size:40px;'>Sugar Data Dashboard - NCDEX</h1>", unsafe_allow_html=True)

# Load Excel file
df = pd.read_excel("Sugar Prices.xlsx")

# Standardize column names
df.columns = df.columns.str.strip()
df.rename(columns={
    "Calender year": "Calendar Year",
    "Calendar Quarter ": "Calendar Quarter",
    "Kohlapur (S) ": "Kohlapur (S)"
}, inplace=True)

# Ensure correct data types
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df = df.dropna(subset=["Date"])
df = df.sort_values("Date")

# Convert categorical columns to strings
df["Month"] = df["Month"].astype(str)
df["Calendar Year"] = df["Calendar Year"].astype(str)
df["FY"] = df["FY"].astype(str)
df["Calendar Quarter"] = df["Calendar Quarter"].astype(str)
df["Crop Year"] = df["Crop Year"].astype(str)

# Convert "Kohlapur (S)" to numeric
df["Kohlapur (S)"] = pd.to_numeric(df["Kohlapur (S)"], errors='coerce')

# Section heading
st.subheader("📊 Latest Trading Data")

# Extract latest row
latest_row = df.iloc[-1]

# Extract values for metric display
last_price_value = latest_row["Kohlapur (S)"]
latest_date = latest_row["Date"].strftime("%Y-%m-%d")
latest_month = latest_row["Month"]
latest_fy = latest_row["FY"]

# Extract previous day's data for comparison
previous_row = df.iloc[-2] if len(df) > 1 else latest_row
previous_price = previous_row["Kohlapur (S)"]

# Calculate percentage change
percentage_change = round(((last_price_value - previous_price) / previous_price) * 100, 2)
delta_value = f"{percentage_change}%"

# Display metric cards
col1, col2, col3, col4 = st.columns(4)
col1.metric(label="Latest Price (Kohlapur)", value=f"{last_price_value:,.2f}", delta=delta_value, delta_color="inverse")
col2.metric(label="Date", value=latest_date)
col3.metric(label="Month", value=latest_month)
col4.metric(label="Fiscal Year (FY)", value=latest_fy)

# Display Data Table with modern styling
st.subheader("📋 Data Table")
st.dataframe(df.style.set_properties(**{
    'background-color': '#1e1e1e',
    'border-color': '#ffa500',
    'border-width': '1px',
    'font-size': '14px',
    'text-align': 'center',
    'color': 'white'
}))

# Drop duplicate dates for the trend chart
unique_dates_df = df.drop_duplicates(subset="Date", keep="first")

# Extract dates & prices for trend analysis
dates = unique_dates_df["Date"].dt.strftime("%Y-%m-%d").tolist()
prices = unique_dates_df["Kohlapur (S)"].tolist()

# Trend Line Chart - Improved for Dark Mode with Correct Labels
st.subheader("📈 Price Trend Over Time")
fig = px.line(
    x=dates,
    y=prices,
    markers=True,
    title="📊 Past Price Trends",
    labels={"x": "Year", "y": "Price"},  # Fix axis labels
    line_shape="spline",
    color_discrete_sequence=["#ffa500"]  # Bright Orange for Visibility
)

# Improve Chart Readability
fig.update_layout(
    plot_bgcolor="#1e1e1e",
    paper_bgcolor="#121212",
    font=dict(color="white"),
    xaxis=dict(
        title="Date",  # X-axis Label
        showgrid=True,
        gridcolor="#444",
        tickangle=-45
    ),
    yaxis=dict(
        title="Price",  # Y-axis Label
        showgrid=True,
        gridcolor="#444"
    ),
    margin=dict(l=40, r=40, t=50, b=40)
)

st.plotly_chart(fig, use_container_width=True)
