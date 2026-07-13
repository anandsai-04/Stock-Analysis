import os
import argparse
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

from agents.analyst_agent import get_financial_analysis

def main():
    parser = argparse.ArgumentParser(description="Test the Quant Finance AI Analyst Agent")
    parser.add_argument("ticker", type=str, help="The stock ticker to analyze (e.g., AAPL, TSLA)")
    parser.add_argument("--provider", type=str, default="openai", choices=["openai", "ollama", "groq", "gemini"], help="The LLM provider to use")
    parser.add_argument("--model", type=str, default="gpt-4o", help="The model name to use (e.g., gpt-4o, llama3, mixtral-8x7b-32768, gemini-1.5-pro)")
    
    args = parser.parse_args()
    
    print(f"==================================================")
    print(f"Analyzing {args.ticker} using {args.provider} ({args.model})...")
    print(f"==================================================\n")
    
    try:
        result = get_financial_analysis(
            ticker=args.ticker,
            provider=args.provider,
            model=args.model
        )
        print(result)
    except Exception as e:
        print(f"\nError: {str(e)}")
        if args.provider == "openai" and "OPENAI_API_KEY" not in os.environ:
            print("Hint: It looks like you forgot to set your OPENAI_API_KEY in the .env file.")

if __name__ == "__main__":
    main()
