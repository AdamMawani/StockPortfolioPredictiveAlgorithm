import yfinance as yf
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt

# Define portfolio
portfolio = {"AAPL": 0.1, "TSLA": 0.9}

# Fetch historical data for each stock in the portfolio
start_date = "2020-01-01"
end_date = "2023-01-01"

stock_data = {}
for ticker, weight in portfolio.items():
    data = yf.download(ticker, start=start_date, end=end_date)
    stock_data[ticker] = {'data': data, 'weight': weight}

# Calculate daily returns for each stock in the portfolio
returns = pd.DataFrame()
for ticker, stock_info in stock_data.items():
    data = stock_info['data']
    returns[ticker] = data['Adj Close'].pct_change().dropna() * stock_info['weight']

# Drop NaN values
returns = returns.dropna()

# Combine returns to get portfolio returns
returns['Portfolio'] = returns.sum(axis=1)

# Fit ARIMA model to portfolio returns
order = (1, 1, 1)  # ARIMA(p, d, q) order
model = ARIMA(returns['Portfolio'], order=order)
results = model.fit()

# Display model summary
print(results.summary())

# Plot actual vs. predicted portfolio returns
plt.figure(figsize=(12, 6))
plt.plot(returns['Portfolio'], label='Actual Returns')
plt.plot(results.fittedvalues, color='red', label='ARIMA Predicted Returns')
plt.legend()
plt.title('ARIMA Model for Portfolio Returns')
plt.show()
