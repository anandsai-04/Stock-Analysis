import os
from langchain.agents import create_react_agent, AgentExecutor
from langchain.prompts import PromptTemplate
from agents.analyst_agent import get_llm
from tools.financial_tools import market_data_tool, financial_ratio_calculator
# We will import time_series_forecaster and vertical_analysis_tool here later

def create_quant_agent(provider="openai", model="gpt-4o"):
    llm = get_llm(provider, model)
    tools = [market_data_tool, financial_ratio_calculator] 
    
    template = """You are the Quant Data Subagent. Your expertise is in numerical financial analysis and predictive modeling.
When given a ticker, use your tools to fetch current market data, calculate Liquidity, Solvency, Activity, and Profitability ratios, and perform Time Series forecasting.
Return purely data-driven insights. Do not worry about domain context or reading text documents; stick to the math and historical price trends.

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
