import os
from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatOllama
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain.prompts import PromptTemplate

from tools.financial_tools import market_data_tool, financial_statement_tool, financial_ratio_calculator

def get_llm(provider: str, model_name: str):
    provider = provider.lower()
    if provider == "openai":
        # Requires OPENAI_API_KEY environment variable
        return ChatOpenAI(model=model_name, temperature=0)
    elif provider == "ollama":
        # Requires Ollama running locally
        return ChatOllama(model=model_name, temperature=0)
    elif provider == "groq":
        # Requires GROQ_API_KEY environment variable
        return ChatGroq(model_name=model_name, temperature=0)
    elif provider == "gemini":
        # Requires GOOGLE_API_KEY environment variable
        return ChatGoogleGenAI(model=model_name, temperature=0)
    else:
        raise ValueError(f"Unsupported provider: {provider}. Choose from: openai, ollama, groq, gemini.")

def get_financial_analysis(ticker: str, provider: str = "openai", model: str = "gpt-4o") -> str:
    llm = get_llm(provider, model)
    
    tools = [market_data_tool, financial_statement_tool, financial_ratio_calculator]
    
    template = """You are a Senior Quant Finance AI Analyst.
Your goal is to provide a comprehensive, educational, and easy-to-understand financial analysis of a given company.
The user does not have a deep quant finance background, so you must explain the meaning of any ratios or metrics you use in simple English.

When analyzing the company, make sure to cover:
1. **Market Overview**: Current price, market cap, and sector.
2. **Liquidity**: Ability to pay off short-term debts (e.g., Current Ratio). Explain what this means for the company's short-term health.
3. **Solvency**: Long-term financial stability (e.g., Debt-to-Equity). Explain if the company is overly reliant on debt.
4. **Profitability**: How well the company generates profit (e.g., Profit Margin, Return on Equity).

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
When you have a response to say to the Human, or if you do not need to use a tool, you MUST use the format:
```
Thought: Do I need to use a tool? No
Final Answer: [your response here, formatted in markdown with clear headings]
```

Begin!

Question: Analyze the financial health and market data for {ticker}.
Thought: {agent_scratchpad}"""

    prompt = PromptTemplate.from_template(template)
    
    agent = create_react_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)
    
    try:
        result = agent_executor.invoke({"ticker": ticker})
        return result["output"]
    except Exception as e:
        return f"Agent execution failed: {str(e)}"
