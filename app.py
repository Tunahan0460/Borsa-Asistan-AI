import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="AI Stock Analyzer", layout="wide")
st.title("🛡️ BORSA-ASISTAN: AI OPERATION CENTER")
st.markdown("---")

# --- SIDEBAR: CONTROL PANEL ---
st.sidebar.header("📋 Control Panel")
stock_list = ["THYAO.IS", "SASA.IS", "EREGL.IS", "ASELS.IS", "SISE.IS", "AAPL", "TSLA", "BTC-USD"]
selected_stock = st.sidebar.selectbox("Select Stock/Crypto:", stock_list)
time_period = st.sidebar.selectbox("Time Period:", ["1mo", "3mo", "6mo", "1y"])

# --- DATA FETCHING ---
@st.cache_data
def get_data(ticker, period):
    df = yf.download(ticker, period=period, interval="1d")
    return df

data = get_data(selected_stock, time_period)

if not data.empty:
    # --- TECHNICAL ANALYSIS ---
    data['RSI'] = ta.rsi(data['Close'], length=14)
    data['SMA20'] = ta.sma(data['Close'], length=20)
    
    current_price = data['Close'].iloc[-1]
    last_rsi = data['RSI'].iloc[-1]
    last_sma20 = data['SMA20'].iloc[-1]

    # --- AI DECISION ENGINE ---
    signal = "NEUTRAL"
    confidence = "50%"
    status_color = "info"

    if last_rsi < 35 and current_price > last_sma20:
        signal = "STRONG BUY"
        confidence = f"{int(100 - last_rsi)}%"
        status_color = "success"
    elif last_rsi > 65:
        signal = "SELL / TAKE PROFIT"
        confidence = f"{int(last_rsi)}%"
        status_color = "error"
    elif current_price < last_sma20:
        signal = "BEARISH / CAUTION"
        confidence = "75%"
        status_color = "warning"

    # --- UI DISPLAY ---
    col1, col2, col3 = st.columns(3)
    col1.metric("Price", f"{current_price:.2f}")
    col2.metric("RSI", f"{last_rsi:.2f}")
    
    if status_color == "success": st.success(f"AI SIGNAL: {signal} ({confidence})")
    elif status_color == "error": st.error(f"AI SIGNAL: {signal} ({confidence})")
    else: st.info(f"AI SIGNAL: {signal} ({confidence})")

    st.line_chart(data[['Close', 'SMA20']])
    st.write("Targeting 490 LGS score discipline in trading. Stay sharp.")
else:
    st.error("Check ticker name!")
