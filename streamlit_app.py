import streamlit as st
import requests

st.set_page_config(page_title="QuantBlox AI Analyst", page_icon="📈", layout="wide")

st.title("📈 QuantBlox AI Analyst")
st.markdown("Multi-Agent Financial Diagnostics: Time Series, Vertical Analysis & SEC Scraping")

# Sidebar for Settings
with st.sidebar:
    st.header("⚙️ Agent Routing")
    st.markdown("Assign different models to different agents to load balance token limits.")
    
    with st.expander("Quant Agent", expanded=True):
        quant_provider = st.selectbox("Provider", ["openai", "groq", "gemini", "ollama"], key="q_prov")
        quant_model = st.text_input("Model", value="gpt-4o", key="q_mod")
        
    with st.expander("Extraction Agent", expanded=True):
        ext_provider = st.selectbox("Provider", ["gemini", "openai", "groq", "ollama"], key="e_prov")
        ext_model = st.text_input("Model", value="gemini-2.5-flash", key="e_mod")
        
    with st.expander("Domain Agent", expanded=True):
        dom_provider = st.selectbox("Provider", ["groq", "openai", "gemini", "ollama"], key="d_prov")
        dom_model = st.text_input("Model", value="llama-3.3-70b-versatile", key="d_mod")
        
    with st.expander("Supervisor Agent", expanded=True):
        sup_provider = st.selectbox("Provider", ["openai", "groq", "gemini", "ollama"], key="s_prov")
        sup_model = st.text_input("Model", value="gpt-4o", key="s_mod")
    
    st.divider()
    
    st.header("🔑 API Key Manager")
    st.markdown("Store multiple keys. Agents will use the key for their assigned provider.")
    
    with st.expander("OpenAI"):
        openai_key = st.text_input("OpenAI API Key", type="password")
        if st.button("Save OpenAI Key"):
            requests.post("http://127.0.0.1:8000/api/settings/keys", json={"provider": "openai", "key": openai_key})
            st.success("Saved!")
            
    with st.expander("Groq"):
        groq_key = st.text_input("Groq API Key", type="password")
        if st.button("Save Groq Key"):
            requests.post("http://127.0.0.1:8000/api/settings/keys", json={"provider": "groq", "key": groq_key})
            st.success("Saved!")
            
    with st.expander("Google Gemini"):
        gemini_key = st.text_input("Gemini API Key", type="password")
        if st.button("Save Gemini Key"):
            requests.post("http://127.0.0.1:8000/api/settings/keys", json={"provider": "gemini", "key": gemini_key})
            st.success("Saved!")

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
        status_box = st.status("Initializing Analysis...")
        report_placeholder = st.empty()
        
        try:
            payload = {
                "ticker": ticker,
                "competitor_ticker": competitor,
                "quant_provider": quant_provider,
                "quant_model": quant_model,
                "domain_provider": dom_provider,
                "domain_model": dom_model,
                "extraction_provider": ext_provider,
                "extraction_model": ext_model,
                "supervisor_provider": sup_provider,
                "supervisor_model": sup_model
            }
            import json
            response = requests.post("http://127.0.0.1:8000/api/analyze", json=payload, stream=True)
            
            if response.status_code == 200:
                for line in response.iter_lines():
                    if line:
                        data = json.loads(line)
                        if "status" in data:
                            status_box.write(f"🔄 {data['status']}")
                        elif "final_report" in data:
                            status_box.update(label="Analysis Complete!", state="complete", expanded=False)
                            report_placeholder.markdown(data["final_report"])
                        elif "error" in data:
                            status_box.update(label="Error Occurred", state="error")
                            st.error(data["error"])
            else:
                st.error(f"Backend failed with status code: {response.status_code}")
        except Exception as e:
            st.error(f"Connection error: Make sure the FastAPI backend is running! Details: {e}")
