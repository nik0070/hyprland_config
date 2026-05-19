import yfinance as yf
import pandas as pd

stock = yf.Ticker("RELIANCE.NS")

out = stock.quarterly_financials
df = pd.DataFrame(out)

df.to_csv("RELIANCE_quarterly_financials.csv")
print(f"Successfully saved {stock} to CSV")
