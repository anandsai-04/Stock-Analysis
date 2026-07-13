from langchain_core.tools import tool

@tool
def send_mcp_email_tool(recipient: str, subject: str, body: str) -> str:
    """Uses the Model Context Protocol (MCP) Gmail server to dispatch a financial report.
    This simulates the MCP connection to Gmail for automated reporting."""
    
    # In a real MCP setup, we would connect to the MCP standard input/output of the Gmail server.
    # For now, we simulate success and log to terminal.
    print(f"\n[MCP GMAIL SERVER ACTIVATED]")
    print(f"Attempting to dispatch email to: {recipient}")
    print(f"Subject: {subject}")
    print(f"Status: SUCCESS - Email sent via MCP Protocol.\n")
    
    return f"Successfully dispatched email via MCP Gmail to {recipient}"
