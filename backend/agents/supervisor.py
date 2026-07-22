from agents.quant_agent import create_quant_agent
from agents.extraction_agent import create_extraction_agent
from agents.domain_agent import create_domain_agent
from agents.analyst_agent import get_llm
from langchain.schema import HumanMessage

def run_supervisor(ticker: str, competitor_ticker: str = "", provider: str = "openai", model: str = "gpt-4o") -> str:
    """The Supervisor Agent that orchestrates the subagents and synthesizes the final report."""
    
    print(f"--- SUPERVISOR: Initiating Analysis for {ticker} ---")
    
    # 1. Initialize Subagents
    quant_agent = create_quant_agent(provider, model)
    domain_agent = create_domain_agent(provider, model)
    extraction_agent = create_extraction_agent(provider, model)
    
    # 2. Run Quant Agent
    print(f"--- SUPERVISOR: Delegating to Quant Data Agent ---")
    quant_prompt = f"Analyze the financial ratios and market data for {ticker}."
    try:
        quant_result = quant_agent.invoke({"input": quant_prompt})["output"]
    except Exception as e:
        quant_result = f"Quant Agent encountered an error: {str(e)}"
    
    # 3. Run Domain Agent
    print(f"--- SUPERVISOR: Delegating to Domain Intelligence Agent ---")
    if competitor_ticker:
        domain_prompt = f"Evaluate the following quantitative data for {ticker} against its industry baselines, and compare it specifically against {competitor_ticker}:\n{quant_result}"
    else:
        domain_prompt = f"Evaluate the following quantitative data for {ticker} against its industry baselines:\n{quant_result}"
        
    try:
        domain_result = domain_agent.invoke({"input": domain_prompt})["output"]
    except Exception as e:
        domain_result = f"Domain Agent encountered an error: {str(e)}"
    
    # 4. Run Extraction Agent
    print(f"--- SUPERVISOR: Delegating to Document Extraction Agent ---")
    extraction_prompt = f"Search for {ticker}'s latest SEC filings or news and explain any qualitative reasons for the metrics calculated here:\n{quant_result}"
    try:
        extraction_result = extraction_agent.invoke({"input": extraction_prompt})["output"]
    except Exception as e:
        extraction_result = f"Document Extraction Agent encountered an error: {str(e)}"
        
    # 5. Synthesize Final Report
    print(f"--- SUPERVISOR: Synthesizing Final Report ---")
    llm = get_llm(provider, model)
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
    return final_report
