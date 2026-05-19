import pandas as pd
import requests
import json
from thefuzz import process
from pathlib import Path
from tqdm import tqdm

# Setup paths
BASE = Path(__file__).resolve().parent.parent
NSE_MASTER_PATH = BASE / "src/data/static/nse_master.csv"
STOCK_SECTORS_PATH = BASE / "src/data/static/stock_sectors.csv"
OUTPUT_PATH = BASE / "src/data/static/ticker_map.csv"  # Overwrite the old one so fetch_financials just works

# Configuration for local Ollama
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
# Change this to whatever model you have pulled (e.g., "llama3", "mistral", "phi3")
MODEL_NAME = "llama3:latest" 

def query_ollama(company_name: str, options: list) -> str:
    """Asks Ollama to pick the correct NSE ticker from a list of options using numbers."""
    
    # Create a numbered list for the LLM
    options_text = "\n".join([f"{idx + 1}. {name} (Ticker: {ticker})" for idx, (name, ticker) in enumerate(options)])
    
    prompt = f"""
    You are a financial data expert. 
    A web scraper found the company name: "{company_name}".
    
    Here are the closest official NSE company names:
    {options_text}
    
    Your task: Identify which option is the exact same company as "{company_name}".
    
    Rules:
    1. Respond ONLY with the NUMBER of the matching option (e.g., 1, 2, 3).
    2. Do not write any words, tickers, or names. ONLY THE NUMBER.
    3. If none of the options match, respond ONLY with: 0
    """
    
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.0} 
    }
    
    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        result = response.json()["response"].strip()
        
        # Extract the first number found in the LLM's response
        import re
        numbers = re.findall(r'\d+', result)
        
        if not numbers:
            return "UNKNOWN"
            
        choice = int(numbers[0])
        
        # 0 means the LLM decided none of them matched
        if choice == 0 or choice > len(options):
            return "UNKNOWN"
            
        # Return the actual ticker from the options list
        # options is a list of tuples: (Company Name, Ticker)
        return options[choice - 1][1]
        
    except Exception as e:
        print(f"Ollama Error: {e}")
        return "UNKNOWN"

def build_llm_ticker_map():
    print(f"Loading data...")
    nse_df = pd.read_csv(NSE_MASTER_PATH)
    nse_df["NAME OF COMPANY"] = nse_df["NAME OF COMPANY"].str.strip()
    nse_names = nse_df["NAME OF COMPANY"].tolist()
    symbol_lookup = dict(zip(nse_df["NAME OF COMPANY"], nse_df["SYMBOL"].str.strip()))

    sectors_df = pd.read_csv(STOCK_SECTORS_PATH)
    company_names = sectors_df["company"].dropna().unique().tolist()
    
    results = []
    total = len(company_names)
    print(f"Starting LLM mapping for {total} companies using Ollama ({MODEL_NAME})...\n")

    pbar = tqdm(company_names, desc="Mapping Tickers")
    for i, company in enumerate(pbar):
        # --- NEW: First Word Guarantee ---
        # Get the first word, removing any weird punctuation
        first_word = company.split()[0].lower().strip(".,&-")
        
        # Find all NSE names that contain this exact first word
        exact_word_matches = [
            name for name in nse_names 
            if first_word in name.lower().split()
        ]
        
        # 1. Get top 10 fuzzy matches (increased from 5 just to be safe)
        fuzzy_matches = [match[0] for match in process.extract(company, nse_names, limit=10)]
        
        # Combine the lists and remove duplicates
        combined_candidates = list(set(exact_word_matches + fuzzy_matches))
        
        # Format for LLM: [(Name, Ticker), (Name, Ticker), ...]
        options_for_llm = [(name, symbol_lookup[name]) for name in combined_candidates]
        
        # 2. Ask Ollama to pick
        picked_ticker = query_ollama(company, options_for_llm)
        
        # Append .NS if it found a ticker
        final_ticker = f"{picked_ticker}.NS" if picked_ticker != "UNKNOWN" else "UNKNOWN"
        
        # Update progress bar with the latest pick
        pbar.set_postfix({"Picked": final_ticker})
        
        results.append({
            "company": company,
            "ticker": final_ticker
        })
        
        # Save progress periodically
        if (i + 1) % 50 == 0:
             pd.DataFrame(results).to_csv(OUTPUT_PATH, index=False)

    # Final save
    pd.DataFrame(results).to_csv(OUTPUT_PATH, index=False)
    print(f"\nFinished! Saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    build_llm_ticker_map()
