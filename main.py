from bot.services.rsi_calculation_service import RSICalculator

calc = RSICalculator("NVDA", 90)
if calc.fetch_data():
    calc.calculate_rsi(14)
    print(calc.data.tail()[["Close", "RSI_14"]])