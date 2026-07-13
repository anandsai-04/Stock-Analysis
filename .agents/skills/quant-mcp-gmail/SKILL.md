---
name: quant-mcp-gmail
description: Uses the Model Context Protocol (MCP) to draft and automatically dispatch generated financial reports via Gmail.
---

# Quant MCP Gmail Reporting Skill

This skill dictates how to automatically distribute the Supervisor's final financial report to users.

## Workflow

1. **Format Report**: Ensure the final synthesized report from the Supervisor Agent is formatted in clean, professional Markdown or HTML.
2. **Connect MCP**: Utilize the MCP connection to authenticate with the Gmail server.
3. **Draft Email**: Construct the email payload. Include the company ticker and the date in the subject line (e.g., "AI Financial Analysis: AAPL - Oct 24").
4. **Dispatch**: Send the email to the designated user or mailing list.
5. **Confirmation**: Log the successful dispatch or handle any connection errors gracefully.
