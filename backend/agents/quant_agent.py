import os
from langchain.agents import create_react_agent, AgentExecutor
from langchain.prompts import PromptTemplate
from agents.analyst_agent import get_llm
from tools.financial_tools import market_data_tool, financial_ratio_calculator, vertical_analysis_tool
from tools.time_series_tools import prophet_forecaster, arima_forecaster_tool, garch_volatility_tool

def create_quant_agent(provider="openai", model="gpt-4o"):
    llm = get_llm(provider, model)
    tools = [market_data_tool, financial_ratio_calculator, vertical_analysis_tool, prophet_forecaster, arima_forecaster_tool, garch_volatility_tool] 
    
    template = """You are the Quant Data Subagent. Your expertise is in numerical financial analysis and advanced econometric modeling.
When given a ticker, use your tools to fetch current market data, calculate ratios, and perform Vertical Analysis.
Crucially, you must perform a Champion/Challenger Time Series forecast by running BOTH `prophet_forecaster` and `arima_forecaster_tool`, and evaluating risk using `garch_volatility_tool`.
Return purely data-driven insights. Do not worry about domain context or reading text documents; stick to the math, econometrics, and historical price trends.

TOOLS:
------
You have access to the following tools:
{tools}

To use a tool, please use the following format:
```
Thought: Do I need to use a tool? Yes
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
```
When you have a response to say to the Supervisor, or if you do not need to use a tool, you MUST use the format:
```
Thought: Do I need to use a tool? No
Final Answer: [your data-driven insights here]
```

Begin!

Task: {input}
Thought: {agent_scratchpad}"""
    
    prompt = PromptTemplate.from_template(template)
    agent = create_react_agent(llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)
