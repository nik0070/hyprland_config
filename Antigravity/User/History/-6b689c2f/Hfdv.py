import yfinance as yf

stock = yf.Ticker("RELIANCE.NS")

print(f'Quarterly Financials: {stock.quarterly_financials.head()}')
print(f'Quarterly Balance Sheet: {stock.quarterly_balance_sheet.head()}')
print(f'Info: {stock.info}')
