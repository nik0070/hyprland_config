import pandas as pd
import yfinance as yf
# pyrefly: ignore [missing-import]
from utils.helper_functions import get_path

# Load the ticker map once when the module is imported
TICKER_MAP_PATH = get_path("src/data/static/ticker_map.csv")

if TICKER_MAP_PATH.exists():
    _df = pd.read_csv(TICKER_MAP_PATH)
    _valid = _df[_df["ticker"] != "UNKNOWN"]
    COMPANY_TO_TICKER = dict(zip(_valid["company"], _valid["ticker"]))
else:
    COMPANY_TO_TICKER = {}
    print(f"Warning: Ticker map not found at {TICKER_MAP_PATH}")


def fetch_kpis(company_name: str) -> dict:
    """Fetches ONLY the KPI metrics (PE, PB, Moving Averages, etc.)"""
    ticker_symbol = COMPANY_TO_TICKER.get(company_name)

    if not ticker_symbol:
        return {"status": "Error", "message": f"Ticker not found for '{company_name}'."}

    try:
        stock = yf.Ticker(ticker_symbol)
        info = stock.info
        
        # Get historical data for moving averages
        history = stock.history(period="6mo")
        ma30 = history["Close"].rolling(window=30).mean().iloc[-1] if len(history) >= 30 else None
        ma100 = history["Close"].rolling(window=100).mean().iloc[-1] if len(history) >= 100 else None

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
            "status": "Success"
        }
    except Exception as e:
        return {"status": "Error", "message": f"Failed to fetch KPIs for {ticker_symbol}: {str(e)}"}


def fetch_quarterly_financials(company_name: str) -> dict:
    """Fetches ONLY the Quarterly Financials"""
    ticker_symbol = COMPANY_TO_TICKER.get(company_name)

    if not ticker_symbol:
        return {"status": "Error", "message": f"Ticker not found for '{company_name}'."}

    try:
        stock = yf.Ticker(ticker_symbol)
        qtr_financials = stock.quarterly_financials
        
        if qtr_financials is None or qtr_financials.empty:
            return {"status": "Error", "message": "No quarterly data available for this ticker."}

        return {
            "company_name": company_name,
            "ticker": ticker_symbol,
            "data": qtr_financials.to_dict(),
            "status": "Success"
        }
    except Exception as e:
        return {"status": "Error", "message": f"Failed to fetch financials for {ticker_symbol}: {str(e)}"}

