from fastapi import FastAPI, UploadFile, File, Form, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()  # Auto-load API keys from .env file

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
    competitor_ticker: Optional[str] = ""
    provider: Optional[str] = "openai"
    model: Optional[str] = "gpt-4o"

class ApiKeyRequest(BaseModel):
    provider: str
    key: str

@app.post("/api/settings/keys")
def update_api_key(request: ApiKeyRequest):
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    provider_map = {
        "openai": "OPENAI_API_KEY",
        "groq": "GROQ_API_KEY",
        "gemini": "GOOGLE_API_KEY"
    }
    env_key = provider_map.get(request.provider)
    if not env_key:
        return {"error": "Invalid provider"}
        
    lines = []
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            lines = f.readlines()
            
    updated = False
    for i, line in enumerate(lines):
        if line.startswith(f"{env_key}="):
            lines[i] = f"{env_key}=\"{request.key}\"\n"
            updated = True
            break
            
    if not updated:
        lines.append(f"{env_key}=\"{request.key}\"\n")
        
    with open(env_path, "w") as f:
        f.writelines(lines)
        
    os.environ[env_key] = request.key
    return {"status": "success"}

@app.post("/api/analyze")
async def analyze_ticker(request: AnalysisRequest):
    try:
        report = run_supervisor(request.ticker, request.competitor_ticker, request.provider, request.model)
        return {"analysis": report}
    except Exception as e:
        return {"error": str(e)}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
