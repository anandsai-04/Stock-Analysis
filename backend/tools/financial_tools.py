import yfinance as yf
from langchain_core.tools import tool
from utils.cache import get_cached_company_details, cache_company_details

@tool
def market_data_tool(ticker: str) -> str:
    """Fetches current market data and company info for a given ticker. Use this when you need basic info, sector, or current price."""
    try:
        cached_details = get_cached_company_details(ticker)
        if cached_details:
            return f"[From Cache]\n{cached_details}"

        stock = yf.Ticker(ticker)
        info = stock.info
        name = info.get('longName', 'N/A')
        sector = info.get('sector', 'N/A')
        price = info.get('currentPrice', 'N/A')
        market_cap = info.get('marketCap', 'N/A')
        
        details = f"Company: {name}\nSector: {sector}\nCurrent Price: {price}\nMarket Cap: {market_cap}"
        
        # Cache the details for future use
        cache_company_details(ticker, details)
        
        return details
    except Exception as e:
        return f"Error fetching market data: {str(e)}"

@tool
def financial_statement_tool(ticker: str) -> str:
    """Fetches the latest balance sheet information for the given ticker. Use this to get total assets, liabilities, and equity."""
    try:
        stock = yf.Ticker(ticker)
        bs = stock.balance_sheet
        if bs.empty:
            return "Could not retrieve balance sheet data."
        
        # Get the most recent column
        latest_bs = bs.iloc[:, 0]
        assets = latest_bs.get('Total Assets', 'N/A')
        liabilities = latest_bs.get('Total Liabilities Net Minority Interest', latest_bs.get('Total Liabilities', 'N/A'))
        equity = latest_bs.get('Stockholders Equity', latest_bs.get('Total Stockholder Equity', 'N/A'))
        
        return f"Latest Balance Sheet Info for {ticker}:\nTotal Assets: {assets}\nTotal Liabilities: {liabilities}\nStockholders Equity: {equity}"
    except Exception as e:
        return f"Error fetching financial statement: {str(e)}"

@tool
def financial_ratio_calculator(ticker: str) -> str:
    """Calculates key Activity, Liquidity, Solvency, and Profitability ratios using yfinance data. Use this when asked about financial health, operational efficiency, solvency, liquidity, or profitability."""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # 1. Activity Ratios (Operating Efficiency)
        # yfinance info doesn't always have all turnover ratios directly, but we can extract some or proxy them.
        # We'll provide what's available or note them as N/A.
        inventory_turnover = info.get('inventoryTurnover', 'N/A')
        asset_turnover = info.get('assetTurnover', 'N/A')
        
        # 2. Liquidity Ratios
        current_ratio = info.get('currentRatio', 'N/A')
        quick_ratio = info.get('quickRatio', 'N/A')
        
        # 3. Solvency Ratios
        debt_to_equity = info.get('debtToEquity', 'N/A')
        debt_to_assets = "N/A" # Derived manually if needed, but not always in info
        
        # 4. Profitability Ratios
        gross_margin = info.get('grossMargins', 'N/A')
        operating_margin = info.get('operatingMargins', 'N/A')
        net_profit_margin = info.get('profitMargins', 'N/A')
        return_on_assets = info.get('returnOnAssets', 'N/A')
        return_on_equity = info.get('returnOnEquity', 'N/A')
        
        report = f"Calculated Ratios for {ticker}:\n"
        report += f"\n--- 1. Activity Ratios ---\n"
        report += f"Inventory Turnover: {inventory_turnover}\n"
        report += f"Asset Turnover: {asset_turnover}\n"
        
        report += f"\n--- 2. Liquidity Ratios ---\n"
        report += f"Current Ratio: {current_ratio}\n"
        report += f"Quick Ratio: {quick_ratio}\n"
        
        report += f"\n--- 3. Solvency Ratios ---\n"
        report += f"Debt-to-Equity: {debt_to_equity}\n"
        # Activity Ratios
        inventory = info.get("inventory", 0)
        cogs = info.get("costOfRevenue", 0)
        
        ratios = f"--- Financial Ratios for {ticker} ---\n"
        ratios += f"Liquidity - Current Ratio: {current_ratio}\n"
        ratios += f"Solvency - Debt to Equity: {debt_to_equity}\n"
        ratios += f"Profitability - Profit Margin: {profit_margin}%\n"
        ratios += f"Profitability - ROE: {roe}%\n"
        
        return ratios
    except Exception as e:
        return f"Error calculating ratios: {str(e)}"

@tool
def vertical_analysis_tool(ticker: str) -> str:
    """Performs Vertical Analysis (Common-Size Income Statement) for a company.
    Converts all major expenses (COGS, SG&A) into a percentage of Total Revenue."""
    try:
        company = yf.Ticker(ticker)
        income_stmt = company.financials
        
        if income_stmt is None or income_stmt.empty:
            return f"No financial statement data available for {ticker}"
            
        latest_year = income_stmt.columns[0]
        data = income_stmt[latest_year]
        
        total_revenue = data.get("Total Revenue", 0)
        if total_revenue == 0:
            return "Total Revenue is 0 or missing, cannot perform vertical analysis."
            
        cogs = data.get("Cost Of Revenue", 0)
        gross_profit = data.get("Gross Profit", 0)
        sga = data.get("Selling General And Administration", 0)
        operating_income = data.get("Operating Income", 0)
        net_income = data.get("Net Income", 0)
        
        cogs_pct = round((cogs / total_revenue) * 100, 2)
        gross_pct = round((gross_profit / total_revenue) * 100, 2)
        sga_pct = round((sga / total_revenue) * 100, 2)
        op_inc_pct = round((operating_income / total_revenue) * 100, 2)
        net_inc_pct = round((net_income / total_revenue) * 100, 2)
        
        report = f"--- Vertical Analysis (Common-Size) for {ticker} ---\n"
        report += f"Total Revenue: 100%\n"
        report += f"Cost of Revenue (COGS): {cogs_pct}% of Revenue\n"
        report += f"Gross Profit Margin: {gross_pct}%\n"
        report += f"SG&A Expenses: {sga_pct}% of Revenue\n"
        report += f"Operating Margin: {op_inc_pct}%\n"
        report += f"Net Profit Margin: {net_inc_pct}%\n"
        
        return report
    except Exception as e:
        return f"Error performing vertical analysis: {str(e)}"
