# QuantBlox AI — Multi-Agent Financial Analyst

An AI-powered financial analysis platform using a Supervisor-Subagent architecture to deliver institutional-grade equity research reports.

## Features
- **Multi-Agent System**: Supervisor orchestrates Quant, Domain, and Extraction subagents
- **Time Series Forecasting**: Prophet (seasonality), ARIMA with Random Search (directional), GARCH (volatility)
- **Vertical Analysis**: Common-size income statements (% of revenue)
- **Peer Comparison**: User-selected competitor side-by-side analysis
- **Domain Intelligence**: Industry-specific ratio baselines (Tech, Finance, EV, Healthcare)
- **SEC Document Scraping**: DuckDuckGo search + PDF/HTML extraction for MD&A
- **Multi-LLM Support**: OpenAI, Groq, Gemini, Ollama

## Quick Start

```bash
# 1. Clone
git clone https://github.com/anandsai-04/Stock-Analysis.git
cd Stock-Analysis

# 2. Set up Python environment
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r ../requirements.txt

# 3. Add your API key
cp .env.example .env
# Edit .env with your OpenAI/Groq/Gemini key

# 4. Start the backend
uvicorn main:app --reload

# 5. Start the frontend (new terminal)
cd ..
source backend/.venv/bin/activate
streamlit run streamlit_app.py
```

## Architecture
```
User (Streamlit) → FastAPI → Supervisor Agent
                                ├── Quant Agent (ratios, Prophet, ARIMA, GARCH)
                                ├── Domain Agent (baselines, peer comparison)
                                └── Extraction Agent (SEC filings, MD&A)
                              → LLM Synthesis → Final Markdown Report
```

## API Endpoints
| Method | Route | Purpose |
|--------|-------|---------|
| POST | `/api/analyze` | Run full multi-agent analysis |
| POST | `/api/settings/keys` | Save API key to .env |
| GET | `/health` | Health check |
