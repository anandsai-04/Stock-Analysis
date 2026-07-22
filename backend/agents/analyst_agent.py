import os
from langchain_openai import ChatOpenAI
try:
    from langchain_ollama import ChatOllama
except ImportError:
    ChatOllama = None
try:
    from langchain_groq import ChatGroq
except ImportError:
    ChatGroq = None
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
except ImportError:
    ChatGoogleGenerativeAI = None
from langgraph.prebuilt import create_react_agent

from tools.financial_tools import market_data_tool, financial_statement_tool, financial_ratio_calculator

def get_llm(provider: str, model_name: str):
    provider = provider.lower()
    if provider == "openai":
        return ChatOpenAI(model=model_name, temperature=0)
    elif provider == "ollama":
        if ChatOllama is None:
            raise ImportError("Install langchain-ollama: pip install langchain-ollama")
        return ChatOllama(model=model_name, temperature=0)
    elif provider == "groq":
        if ChatGroq is None:
            raise ImportError("Install langchain-groq: pip install langchain-groq")
        return ChatGroq(model_name=model_name, temperature=0)
    elif provider == "gemini":
        if ChatGoogleGenerativeAI is None:
            raise ImportError("Install langchain-google-genai: pip install langchain-google-genai")
        return ChatGoogleGenerativeAI(model=model_name, temperature=0)
    else:
        raise ValueError(f"Unsupported provider: {provider}. Choose from: openai, ollama, groq, gemini.")

def get_financial_analysis(ticker: str, provider: str = "openai", model: str = "gpt-4o") -> str:
    llm = get_llm(provider, model)
    tools = [market_data_tool, financial_statement_tool, financial_ratio_calculator]
    
    system_prompt = """You are a Senior Quant Finance AI Analyst.
Your goal is to provide a comprehensive, educational, and easy-to-understand financial analysis of a given company.
The user does not have a deep quant finance background, so you must explain the meaning of any ratios or metrics you use in simple English.

When analyzing the company, make sure to cover:
1. **Market Overview**: Current price, market cap, and sector.
2. **Liquidity**: Ability to pay off short-term debts (e.g., Current Ratio).
3. **Solvency**: Long-term financial stability (e.g., Debt-to-Equity).
4. **Profitability**: How well the company generates profit (e.g., Profit Margin, Return on Equity).
"""
    
    agent = create_react_agent(llm, tools, prompt=system_prompt)
    try:
        result = agent.invoke({"messages": [{"role": "user", "content": f"Analyze the financial health and market data for {ticker}."}]})
        return result["messages"][-1].content
    except Exception as e:
        return f"Agent execution failed: {str(e)}"
