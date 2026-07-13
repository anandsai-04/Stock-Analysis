---
name: quant-document-extraction
description: Extracts qualitative insights, driving factors, and corporate subsidiaries from SEC filings (10-K, 10-Q) using web search, web scraping, and LangChain parsing.
---

# Quant Document Extraction Skill

This skill dictates how to perform deep qualitative research on a company.

## Workflow

1. **Search**: Use DuckDuckGo to search for the specific SEC filing, e.g., "AAPL 2023 10-K SEC.gov".
2. **Fetch**: Download the HTML or PDF document.
3. **Parse**: Extract the text. Due to token limits, focus on specific sections.
4. **MD&A Targeting**: Specifically target the "Management's Discussion and Analysis of Financial Condition and Results of Operations" (MD&A) section.
5. **Causal Analysis**: Extract qualitative statements explaining *why* specific metrics (revenue, COGS, interest) changed year-over-year.
6. **Subsidiary Mapping**: Search the document or the web to map out the company's corporate structure and subsidiaries.
7. **Cache**: Store the summarized findings in Pinecone for quick retrieval by other agents.
