import streamlit as st
import pandas as pd
import plotly.express as px

# Set Streamlit page layout
st.set_page_config(page_title="Sugar Data Dashboard", layout="wide")

# Path to the Hector Beverages logo
logo_path = "hector_logo.png"

# Custom CSS for White Data Table and Dark Theme
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

        /* White Background for Data Table */
        .dataframe {
            background-color: white !important;
            color: black !important;
            border-radius: 10px;
            text-align: center;
            border: 1px solid #ffa500;
        }
    </style>
""", unsafe_allow_html=True)

# Display Logo and Title
col1, col2 = st.columns([0.2, 0.8])
with col1:
    st.image(logo_path, width=120)
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

# Extract previous day's data for comparison
previous_row = df.iloc[-2] if len(df) > 1 else latest_row
previous_price = previous_row["Kohlapur (S)"]

# Calculate percentage change
percentage_change = round(((last_price_value - previous_price) / previous_price) * 100, 2)
delta_value = f"{percentage_change}%"

# Display metric cards (Removed Month & Fiscal Year)
col1, col2 = st.columns(2)
col1.metric(label="Latest Price (Kohlapur)", value=f"{last_price_value:,.2f}", delta=delta_value, delta_color="inverse")
col2.metric(label="Date", value=latest_date)

# 📅 **User Manual Date Entry (Placed Below Latest Price)**
st.subheader("📅 Check Sugar Price for a Specific Date")

# Date Selection
selected_date = st.date_input("Enter Date", key="manual_date_input")

# Convert selected date to DataFrame format
selected_date = pd.to_datetime(selected_date)

# Check if the selected date exists in the dataset
if (df["Date"] == selected_date).any():
    selected_price = df[df["Date"] == selected_date]["Kohlapur (S)"].values[0]
    st.success(f"✅ The price on {selected_date.strftime('%Y-%m-%d')} was **₹ {selected_price:,.2f}**")
else:
    st.error("❌ No data available for the selected date. Please choose another date.")

# Create two columns for **Data Table & Line Chart**
col1, col2 = st.columns([0.6, 0.4])

with col1:
    st.subheader("📋 Data Table")
    
    # **White Data Table Styling**
    df_styled = df.style.set_properties(**{
        'background-color': 'white',
        'color': 'black',
        'border': '1px solid #ffa500',
        'text-align': 'center',
        'font-size': '14px'
    })
    
    st.dataframe(df_styled)

with col2:
    # Drop duplicate dates for the trend chart
    unique_dates_df = df.drop_duplicates(subset="Date", keep="first")

    # Extract dates & prices for trend analysis
    dates = unique_dates_df["Date"].dt.strftime("%Y-%m-%d").tolist()
    prices = unique_dates_df["Kohlapur (S)"].tolist()

    # **Trend Line Chart - Normal Line + White Background**
    st.subheader("📈 Price Trend")
    fig = px.line(
        x=dates,
        y=prices,
        title="📊 Price Trend Over Time",
        labels={"x": "Date", "y": "Price"},
        line_shape="linear",  # **Normal Line Shape**
        color_discrete_sequence=["#ffa500"]  # **Bright Orange**
    )

    # **Normal Line Width (Thin)**
    fig.update_traces(
        line=dict(width=2)  # **Thin Line**
    )

    # **White Background for Chart**
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color="black"),  # **Black Text for Contrast**
        xaxis=dict(
            title="Date",
            showgrid=True,
            gridcolor="#DDD",
            tickangle=-45
        ),
        yaxis=dict(
            title="Price",
            showgrid=True,
            gridcolor="#DDD"
        ),
        margin=dict(l=40, r=40, t=50, b=40)
    )

    st.plotly_chart(fig, use_container_width=True)




    # Simple Trend Estimator (Next 7 Days Based on 30-day Change)
price_trend = df["Kohlapur (S)"].pct_change(periods=30).mean()
future_prices = [df.iloc[-1]["Kohlapur (S)"] * (1 + price_trend) ** i for i in range(1, 8)]
future_dates = pd.date_range(start=df["Date"].max(), periods=7, freq="D")

# Create DataFrame
future_df = pd.DataFrame({"Date": future_dates, "Estimated Price": future_prices})

# Plot
st.subheader("📈 Estimated Price for Next 7 Days (Trend-Based)")
fig = px.line(future_df, x="Date", y="Estimated Price", title="📊 Projected Prices",
              labels={"Date": "Date", "Estimated Price": "Price"}, color_discrete_sequence=["#ff5733"])
st.plotly_chart(fig, use_container_width=True)

