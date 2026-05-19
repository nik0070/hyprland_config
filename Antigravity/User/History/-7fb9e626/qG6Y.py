import pandas as pd
import yfinance as yf
from utils.helper_functions import get_path

# Load the ticker map once when the module is imported
TICKER_MAP_PATH = get_path("src/data/static/ticker_map.csv")

# Create a dictionary for O(1) lookups: {"Hindustan Unilever": "HINDUNILVR.NS"}
if TICKER_MAP_PATH.exists():
    _df = pd.read_csv(TICKER_MAP_PATH)
    # Only keep valid tickers
    _valid = _df[_df["ticker"] != "UNKNOWN"]
    COMPANY_TO_TICKER = dict(zip(_valid["company"], _valid["ticker"]))
else:
    COMPANY_TO_TICKER = {}
    print(f"Warning: Ticker map not found at {TICKER_MAP_PATH}")


def fetch_financials(company_name: str) -> dict:
    """
    Fetches financial data for a given company name using yfinance.
    Uses the pre-built ticker_map.csv to resolve the name to an NSE ticker.
    """
    ticker_symbol = COMPANY_TO_TICKER.get(company_name)

    if not ticker_symbol:
        return {"status": "Error", "message": f"Ticker not found for '{company_name}'. Check ticker_map.csv."}

    try:
        stock = yf.Ticker(ticker_symbol)
        info = stock.info
        
        # Get historical data for moving averages
        history = stock.history(period="6mo")
        ma30 = history["Close"].rolling(window=30).mean().iloc[-1] if len(history) >= 30 else None
        ma100 = history["Close"].rolling(window=100).mean().iloc[-1] if len(history) >= 100 else None

        # Fetch quarterly financials and convert to dict for easy JSON serialization
        qtr_financials = stock.quarterly_financials
        qtr_financials_dict = qtr_financials.to_dict() if qtr_financials is not None and not qtr_financials.empty else {}

        return {
            "company_name": company_name,
            "ticker": ticker_symbol,
            "current_price": info.get("currentPrice"),
            "market_cap": info.get("marketCap"),
            "pe_ratio": info.get("trailingPE"),
            "pb_ratio": info.get("priceToBook"),
            "peg_ratio": info.get("pegRatio"),
            "ma30": ma30,
            "ma100": ma100,
            "quarterly_financials": qtr_financials_dict,
            "status": "Success"
        }
    except Exception as e:
        return {"status": "Error", "message": f"Failed to fetch data for {ticker_symbol}: {str(e)}"}

if __name__ == "__main__":
    # Test with a known company
    print("Testing fetch_financials with 'Reliance Industries'...")
    # Make sure this exact string exists in your stock_sectors.csv/ticker_map.csv
    # Depending on your screener data, it might be "Reliance Industrie" or similar.
    # Let's test with a common one that usually maps well:
    test_company = "Hindustan Unilever" 
    result = fetch_financials(test_company)
    print(result)
