import json
from agents.quant_agent import create_quant_agent
from agents.extraction_agent import create_extraction_agent
from agents.domain_agent import create_domain_agent
from agents.analyst_agent import get_llm
from langchain_core.messages import HumanMessage

def run_supervisor(
    ticker: str, 
    competitor_ticker: str = "", 
    quant_provider: str = "openai",
    quant_model: str = "gpt-4o",
    domain_provider: str = "openai",
    domain_model: str = "gpt-4o",
    extraction_provider: str = "openai",
    extraction_model: str = "gpt-4o",
    supervisor_provider: str = "openai",
    supervisor_model: str = "gpt-4o"
):
    """The Supervisor Agent that orchestrates the subagents and yields real-time progress."""
    
    yield json.dumps({"status": f"Initializing Subagents for {ticker}..."}) + "\n"
    
    # 1. Initialize Subagents with their dedicated LLMs
    quant_agent = create_quant_agent(quant_provider, quant_model)
    domain_agent = create_domain_agent(domain_provider, domain_model)
    extraction_agent = create_extraction_agent(extraction_provider, extraction_model)
    
    # 2. Run Quant Agent
    yield json.dumps({"status": f"Delegating to Quant Data Agent ({quant_model})... fetching market data & running econometrics..."}) + "\n"
    quant_prompt = f"Analyze the financial ratios and market data for {ticker}."
    try:
        quant_res = quant_agent.invoke({"messages": [("user", quant_prompt)]})
        quant_result = quant_res["messages"][-1].content
    except Exception as e:
        quant_result = f"Quant Agent encountered an error: {str(e)}"
    
    # 3. Run Domain Agent
    yield json.dumps({"status": f"Delegating to Domain Intelligence Agent ({domain_model})... evaluating against industry baselines..."}) + "\n"
    if competitor_ticker:
        domain_prompt = f"Evaluate the following quantitative data for {ticker} against its industry baselines, and compare it specifically against {competitor_ticker}:\n{quant_result}"
    else:
        domain_prompt = f"Evaluate the following quantitative data for {ticker} against its industry baselines:\n{quant_result}"
        
    try:
        domain_res = domain_agent.invoke({"messages": [("user", domain_prompt)]})
        domain_result = domain_res["messages"][-1].content
    except Exception as e:
        domain_result = f"Domain Agent encountered an error: {str(e)}"
    
    # 4. Run Extraction Agent
    yield json.dumps({"status": f"Delegating to Document Extraction Agent ({extraction_model})... scraping SEC filings and news..."}) + "\n"
    extraction_prompt = f"Search for {ticker}'s latest SEC filings or news and explain any qualitative reasons for the metrics calculated here:\n{quant_result}"
    try:
        extraction_res = extraction_agent.invoke({"messages": [("user", extraction_prompt)]})
        extraction_result = extraction_res["messages"][-1].content
    except Exception as e:
        extraction_result = f"Document Extraction Agent encountered an error: {str(e)}"
        
    # 5. Synthesize Final Report
    yield json.dumps({"status": f"Synthesizing Final Report using Supervisor ({supervisor_model})..."}) + "\n"
    llm = get_llm(supervisor_provider, supervisor_model)
    synthesis_prompt = f"""You are the Lead Supervisor of a Quant Finance AI system. 
Synthesize the findings of your subagents into a highly professional, comprehensive Markdown report for {ticker}.
    
    Quant Data Findings:
    {quant_result}
    
    Domain Expert Findings:
    {domain_result}
    
    Document Extraction Findings:
    {extraction_result}
    
    Format the report with clear headings (e.g., 'Quantitative Overview', 'Industry & Domain Context', 'Qualitative & Causal Analysis').
    Avoid repeating yourself. Ensure it sounds like a cohesive analysis from a top-tier financial firm.
    Include a disclaimer that this is AI-generated and not financial advice.
    """
    
    final_report = llm.invoke([HumanMessage(content=synthesis_prompt)]).content
    yield json.dumps({"final_report": final_report}) + "\n"
