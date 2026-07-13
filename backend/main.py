from fastapi import FastAPI, UploadFile, File, Form, Depends
from pydantic import BaseModel
from typing import Optional

from agents.analyst_agent import get_financial_analysis

app = FastAPI(title="Quant Finance AI Analyst")

class AnalysisRequest(BaseModel):
    ticker: str
    provider: str = "openai" # "openai" or "ollama"
    model: str = "gpt-4o" # or "llama3" etc.

@app.get("/")
def read_root():
    return {"message": "Quant Finance AI Analyst API is running."}

@app.post("/api/analyze")
def analyze_ticker(request: AnalysisRequest):
    try:
        result = get_financial_analysis(
            ticker=request.ticker,
            provider=request.provider,
            model=request.model
        )
        return {"analysis": result}
    except Exception as e:
        return {"error": str(e)}
