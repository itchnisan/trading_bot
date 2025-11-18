import pandas as pd
import numpy as np
import yfinance as yf
import talib
from datetime import datetime, timedelta

class RSICalculator:
    def __init__(self, ticker_symbol, period_days=90):
        self.ticker_symbol = ticker_symbol
        self.period_days = period_days
        self.data = None

    def fetch_data(self):
        try:
            ticker = yf.Ticker(self.ticker_symbol)
            end_date = datetime.now()
            start_date = end_date - timedelta(days=self.period_days)
            self.data = ticker.history(start=start_date, end=end_date)
            if self.data.empty:
                raise ValueError("No data fetched for the given ticker symbol.")
            return True
        except Exception as e:
            print(f"Error fetching data: {e}")
            return False
    
    def calculate_rsi(self, window=14, column="Close"):
        """Calculate RSI using TA-Lib"""
        if self.data is None:
            raise ValueError("Data not fetched. Call fetch_data() first.")
        
        prices = self.data[column].values
        rsi = talib.RSI(prices, timeperiod=window)
        self.data[f"RSI_{window}"] = rsi
        return rsi