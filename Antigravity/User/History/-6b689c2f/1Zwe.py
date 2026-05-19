import yfinance as yf

stock = yf.Ticker("RELIANCE.NS")

print(f'Quarterly Financials: {stock.quarterly_financials}')
