import os
from langgraph.prebuilt import create_react_agent
from agents.analyst_agent import get_llm
from tools.domain_tools import fetch_domain_baselines, peer_comparison_tool

def create_domain_agent(provider="openai", model="gpt-4o"):
    llm = get_llm(provider, model)
    tools = [fetch_domain_baselines, peer_comparison_tool] 
    
    system_prompt = """You are the Lead Domain Intelligence Subagent. Your expertise is in industry-specific financial standards (Tech, Finance, EV, etc.).
Your job is to evaluate if raw financial ratios (provided by the Supervisor) are healthy *for that specific industry*. 
CRITICAL MANDATES:
1. If a competitor ticker is provided, you MUST execute `peer_comparison_tool` and explicitly report the side-by-side numerical differences.
2. Compare the company against typical sector baselines and explain why certain metrics might be normal for their specific domain.
3. DO NOT hallucinate numbers. Rely ONLY on the numbers provided to you or retrieved by your tools."""

    agent = create_react_agent(llm, tools, prompt=system_prompt)
    return agent
