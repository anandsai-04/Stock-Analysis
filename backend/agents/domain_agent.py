import os
from langchain.agents import create_react_agent, AgentExecutor
from langchain.prompts import PromptTemplate
from agents.analyst_agent import get_llm
from tools.domain_tools import fetch_domain_baselines, peer_comparison_tool

def create_domain_agent(provider="openai", model="gpt-4o"):
    llm = get_llm(provider, model)
    tools = [fetch_domain_baselines, peer_comparison_tool] 
    
    template = """You are the Domain Intelligence Subagent. Your expertise is in industry-specific financial standards (Tech, Finance, EV, etc.).
Your job is to evaluate if raw financial ratios (provided by the Supervisor) are healthy *for that specific industry*. 
Compare the company against typical sector baselines and explain why certain metrics might be normal for their specific domain.

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
Final Answer: [your contextualized industry analysis here]
```

Begin!

Task: {input}
Thought: {agent_scratchpad}"""
    
    prompt = PromptTemplate.from_template(template)
    agent = create_react_agent(llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)
