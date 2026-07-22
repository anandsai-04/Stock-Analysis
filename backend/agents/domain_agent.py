import os
from langgraph.prebuilt import create_react_agent
from agents.analyst_agent import get_llm
from tools.domain_tools import fetch_domain_baselines, peer_comparison_tool

def create_domain_agent(provider="openai", model="gpt-4o"):
    llm = get_llm(provider, model)
    tools = [fetch_domain_baselines, peer_comparison_tool] 
    
    system_prompt = """You are the Domain Intelligence Subagent. Your expertise is in industry-specific financial standards (Tech, Finance, EV, etc.).
Your job is to evaluate if raw financial ratios (provided by the Supervisor) are healthy *for that specific industry*. 
Compare the company against typical sector baselines and explain why certain metrics might be normal for their specific domain."""

    agent = create_react_agent(llm, tools, prompt=system_prompt)
    return agent
