import yfinance as yf
import pandas as pd

stock = yf.Ticker("RELIANCE.NS")
info = stock.info

print({
    "ticker": "RELIANCE.NS",
    "price": info.get("currentPrice"),
    "market_cap": info.get("marketCap"),
    "pe": info.get("trailingPE"),
    "pb": info.get("priceToBook"),
    "peg": info.get("pegRatio")
})
