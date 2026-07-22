import os
from langgraph.prebuilt import create_react_agent
from agents.analyst_agent import get_llm
from tools.financial_tools import market_data_tool, financial_ratio_calculator, vertical_analysis_tool
from tools.time_series_tools import prophet_forecaster, arima_forecaster_tool, garch_volatility_tool

def create_quant_agent(provider="openai", model="gpt-4o"):
    llm = get_llm(provider, model)
    tools = [market_data_tool, financial_ratio_calculator, vertical_analysis_tool, prophet_forecaster, arima_forecaster_tool, garch_volatility_tool] 
    
    system_prompt = """You are the Quant Data Subagent. Your expertise is in numerical financial analysis and advanced econometric modeling.
When given a ticker, use your tools to fetch current market data, calculate ratios, and perform Vertical Analysis.
Crucially, you must perform a Champion/Challenger Time Series forecast by running BOTH `prophet_forecaster` and `arima_forecaster_tool`, and evaluating risk using `garch_volatility_tool`.
Return purely data-driven insights. Do not worry about domain context or reading text documents; stick to the math, econometrics, and historical price trends."""

    agent = create_react_agent(llm, tools, prompt=system_prompt)
    return agent
