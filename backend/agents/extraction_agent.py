import os
from langgraph.prebuilt import create_react_agent
from agents.analyst_agent import get_llm
from tools.web_tools import search_financial_report_tool, download_and_extract_text_tool

def create_extraction_agent(provider="openai", model="gpt-4o"):
    llm = get_llm(provider, model)
    tools = [search_financial_report_tool, download_and_extract_text_tool] 
    
    system_prompt = """You are the Lead Document Extraction Subagent. Your expertise is finding, reading, and extracting hard facts from complex financial documents on the internet.
When asked to research a company, search the web for their latest SEC 10-K, earnings call transcripts, or financial news.
CRITICAL MANDATES:
1. You MUST extract specific, verbatim qualitative statements explaining *why* metrics (like Revenue or Profit) changed.
2. Provide hard proofs (quotes) for your reasoning. Do not guess.
3. You are also responsible for identifying the company's subsidiaries and corporate structure based on real documents."""

    agent = create_react_agent(llm, tools, prompt=system_prompt)
    return agent
