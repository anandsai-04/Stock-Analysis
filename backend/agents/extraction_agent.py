import os
from langchain.agents import create_react_agent, AgentExecutor
from langchain.prompts import PromptTemplate
from agents.analyst_agent import get_llm
from tools.web_tools import search_financial_report_tool, download_and_extract_text_tool
# We will import pinecone_cache_tool here later

def create_extraction_agent(provider="openai", model="gpt-4o"):
    llm = get_llm(provider, model)
    tools = [search_financial_report_tool, download_and_extract_text_tool] 
    
    template = """You are the Document Extraction Subagent. Your expertise is finding, reading, and extracting information from complex financial documents on the internet.
When asked to research a company, search the web for their latest SEC 10-K or Annual Report PDF. Download the document, parse the text, and extract specific qualitative statements explaining *why* metrics changed (MD&A section).
You are also responsible for identifying the company's subsidiaries and corporate structure.

TOOLS:
------
You have access to the following tools:
{tools}

To use a tool, please use the following format:
```
Thought: Do I need to use a tool? Yes
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
```
When you have a response to say to the Supervisor, or if you do not need to use a tool, you MUST use the format:
```
Thought: Do I need to use a tool? No
Final Answer: [your qualitative insights here]
```

Begin!

Task: {input}
Thought: {agent_scratchpad}"""
    
    prompt = PromptTemplate.from_template(template)
    agent = create_react_agent(llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)
