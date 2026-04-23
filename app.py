import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# Page config
st.set_page_config(page_title="Stock Dashboard", layout="wide")

st.title("📈 Real-Time Stock Market Dashboard")

# Sidebar inputs
st.sidebar.header("User Input")

stock = st.sidebar.text_input("Enter Stock Symbol", "AAPL")

period = st.sidebar.selectbox(
    "Select Time Period",
    ["1d", "5d", "1mo", "3mo", "6mo", "1y"]
)

# Fetch data
data = yf.download(stock, period=period)

# Check if data exists
if data.empty:
    st.error("Invalid stock symbol or no data found.")
else:
    # Show company info
    ticker = yf.Ticker(stock)
    info = ticker.info

    st.subheader("📊 Company Information")

    col1, col2, col3 = st.columns(3)

    col1.metric("Current Price", info.get("currentPrice", "N/A"))
    col2.metric("Market Cap", info.get("marketCap", "N/A"))
    col3.metric("Previous Close", info.get("previousClose", "N/A"))

    st.write("**Company Name:**", info.get("longName", "N/A"))
    st.write("**Sector:**", info.get("sector", "N/A"))

    # Plot graph
    st.subheader("📉 Stock Price Chart")

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=data.index,
        y=data["Close"],
        name="Close Price"
    ))

    # Moving Average
    data["MA50"] = data["Close"].rolling(window=50).mean()

    fig.add_trace(go.Scatter(
        x=data.index,
        y=data["MA50"],
        name="Moving Avg (50)"
    ))

    st.plotly_chart(fig, use_container_width=True)

    # Volume chart
    st.subheader("📦 Volume")

    st.bar_chart(data["Volume"])

    # Show raw data
    with st.expander("Show Raw Data"):
        st.write(data.tail())