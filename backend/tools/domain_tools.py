import yfinance as yf
from langchain_core.tools import tool
from typing import Optional

@tool
def fetch_domain_baselines(sector: str) -> str:
    """Retrieves typical ratio ranges for a given industry sector."""
    baselines = {
        "Technology": "High P/E (20-30), Low Debt-to-Equity (< 0.5), High R&D spend.",
        "Financial Services": "High Debt-to-Equity is normal (leverage), focus on Net Interest Margin.",
        "Healthcare": "Steady cash flow, high P/E during drug trials.",
        "Consumer Cyclical": "Highly dependent on economic cycles, lower P/E, moderate debt."
    }
    return baselines.get(sector, f"No specific baselines found for sector: {sector}. Compare against market averages.")

@tool
def peer_comparison_tool(ticker: str, competitor_ticker: str = "") -> str:
    """Compares the financial profile of a company against a direct competitor.
    Provide both the main ticker and the competitor_ticker (e.g., AAPL and MSFT)."""
    if not competitor_ticker:
        return "You must provide a competitor_ticker to compare against."
        
    try:
        main_company = yf.Ticker(ticker)
        main_info = main_company.info
        sector = main_info.get("sector", "Unknown")
        
        peer_company = yf.Ticker(competitor_ticker)
        peer_info = peer_company.info
        
        comparison = f"--- Peer Comparison: {ticker} vs {competitor_ticker} ---\n"
        comparison += f"Sector: {sector} vs {peer_info.get('sector', 'Unknown')}\n"
        comparison += f"Market Cap: {main_info.get('marketCap', 'N/A')} vs {peer_info.get('marketCap', 'N/A')}\n"
        comparison += f"Trailing P/E: {main_info.get('trailingPE', 'N/A')} vs {peer_info.get('trailingPE', 'N/A')}\n"
        comparison += f"Forward P/E: {main_info.get('forwardPE', 'N/A')} vs {peer_info.get('forwardPE', 'N/A')}\n"
        comparison += f"Profit Margin: {main_info.get('profitMargins', 'N/A')} vs {peer_info.get('profitMargins', 'N/A')}\n"
        comparison += f"Debt to Equity: {main_info.get('debtToEquity', 'N/A')} vs {peer_info.get('debtToEquity', 'N/A')}\n"
        
        return comparison
    except Exception as e:
        return f"Error in peer comparison: {str(e)}"
