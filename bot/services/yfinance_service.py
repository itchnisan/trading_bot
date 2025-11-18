import yfinance as yf

nvda = yf.Ticker('NVDA')
info = nvda.info

print(info.get('currentPrice'))

