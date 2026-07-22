import os
from langgraph.prebuilt import create_react_agent
from agents.analyst_agent import get_llm
from tools.financial_tools import market_data_tool, financial_ratio_calculator, vertical_analysis_tool
from tools.time_series_tools import prophet_forecaster, arima_forecaster_tool, garch_volatility_tool

def create_quant_agent(provider="openai", model="gpt-4o"):
    llm = get_llm(provider, model)
    tools = [market_data_tool, financial_ratio_calculator, vertical_analysis_tool, prophet_forecaster, arima_forecaster_tool, garch_volatility_tool] 
    
    system_prompt = """You are the Lead Quant Data Subagent. Your expertise is in numerical financial analysis, strict accounting, and advanced econometric modeling.
When given a ticker, use your tools to fetch current market data, calculate ratios, and perform Vertical Analysis.
CRITICAL MANDATES:
1. You MUST explicitly output the results of the Vertical Analysis (COGS, SG&A margins).
2. You MUST explicitly output the Year-over-Year (YoY) Revenue and Net Income growth.
3. You must perform a Champion/Challenger Time Series forecast by running BOTH `prophet_forecaster` and `arima_forecaster_tool`, and evaluating risk using `garch_volatility_tool`.
4. DO NOT hallucinate numbers. If a tool returns 'N/A', state 'N/A'.
Return a highly structured, data-driven report."""

    agent = create_react_agent(llm, tools, prompt=system_prompt)
    return agent
