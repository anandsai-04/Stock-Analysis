import streamlit as st
import requests

st.set_page_config(page_title="QuantBlox AI Analyst", page_icon="📈", layout="wide")

st.title("📈 QuantBlox AI Analyst")
st.markdown("Multi-Agent Financial Diagnostics: Time Series, Vertical Analysis & SEC Scraping")

# Sidebar for Settings
with st.sidebar:
    st.header("Settings")
    provider = st.selectbox("AI Provider", ["openai", "groq", "gemini", "ollama"])
    model = st.text_input("Model Name", value="gpt-4o")
    
    if provider != "ollama":
        api_key = st.text_input(f"{provider.upper()} API Key", type="password")
        if st.button("Save API Key"):
            if api_key:
                res = requests.post("http://127.0.0.1:8000/api/settings/keys", json={"provider": provider, "key": api_key})
                if res.status_code == 200:
                    st.success("API Key saved securely!")
                else:
                    st.error("Failed to save API Key.")
            else:
                st.warning("Please enter a key before saving.")

# Main Interface
col1, col2 = st.columns(2)
with col1:
    ticker = st.text_input("Ticker Symbol (e.g., AAPL)", max_chars=10).upper()
with col2:
    competitor = st.text_input("Competitor Ticker (Optional, e.g., MSFT)", max_chars=10).upper()

if st.button("Analyze", type="primary"):
    if not ticker:
        st.warning("Please enter a ticker symbol.")
    else:
        with st.spinner("Synthesizing Report... Executing Prophet Models & Scraping MD&A..."):
            try:
                payload = {
                    "ticker": ticker,
                    "competitor_ticker": competitor,
                    "provider": provider,
                    "model": model
                }
                response = requests.post("http://127.0.0.1:8000/api/analyze", json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    if "error" in data:
                        st.error(f"Error: {data['error']}")
                    else:
                        st.success("Analysis Complete!")
                        st.markdown(data["analysis"])
                else:
                    st.error(f"Backend failed with status code: {response.status_code}")
            except Exception as e:
                st.error(f"Connection error: Make sure the FastAPI backend is running! Details: {e}")
