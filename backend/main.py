from fastapi import FastAPI, UploadFile, File, Form, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from agents.supervisor import run_supervisor

app = FastAPI(title="Quant Finance AI Analyst")

# Add CORS to allow Next.js frontend to talk to FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to the Vercel URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalysisRequest(BaseModel):
    ticker: str
    provider: Optional[str] = "openai"
    model: Optional[str] = "gpt-4o"

@app.post("/api/analyze")
async def analyze_ticker(request: AnalysisRequest):
    try:
        report = run_supervisor(request.ticker, request.provider, request.model)
        return {"analysis": report}
    except Exception as e:
        return {"error": str(e)}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
