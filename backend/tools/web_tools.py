import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
from langchain_core.tools import tool
import PyPDF2
from io import BytesIO

@tool
def search_financial_report_tool(query: str) -> str:
    """Searches the web for a financial report (e.g., 'AAPL 2023 10-K report PDF'). Returns a list of URLs."""
    try:
        results = DDGS().text(query, max_results=5)
        if not results:
            return "No results found."
        
        urls = []
        for r in results:
            urls.append(f"Title: {r.get('title')}\nURL: {r.get('href')}")
        return "\n\n".join(urls)
    except Exception as e:
        return f"Error searching the web: {str(e)}"

@tool
def download_and_extract_text_tool(url: str) -> str:
    """Downloads a document from a URL and extracts text. Supports HTML and PDF. Use this to read the content of a financial report."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        content_type = response.headers.get('Content-Type', '').lower()
        
        if 'application/pdf' in content_type or url.lower().endswith('.pdf'):
            reader = PyPDF2.PdfReader(BytesIO(response.content))
            text = ""
            # Extract first 15 pages to avoid massive token limits
            num_pages = min(15, len(reader.pages))
            for i in range(num_pages):
                page_text = reader.pages[i].extract_text()
                if page_text:
                    text += page_text + "\n"
            if len(reader.pages) > 15:
                text += "\n...[TRUNCATED for token limits]..."
            return text
        else:
            # Assume HTML
            soup = BeautifulSoup(response.content, 'lxml')
            text = soup.get_text(separator='\n', strip=True)
            # Truncate text if too long (e.g. 15000 chars)
            if len(text) > 15000:
                text = text[:15000] + "\n...[TRUNCATED for token limits]..."
            return text
    except Exception as e:
        return f"Error downloading or extracting document: {str(e)}"
