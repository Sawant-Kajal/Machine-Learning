import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf
from matplotlib.animation import FuncAnimation

# Function to fetch stock data
def fetch_stock_data(ticker, start_date, end_date):
    return yf.download(ticker, start=start_date, end=end_date)

# Function to calculate moving average
def calculate_moving_average(data, window):
    return data['Close'].rolling(window=window).mean()

# Function to calculate Bollinger Bands
def calculate_bollinger_bands(data, window, num_std):
    rolling_mean = data['Close'].rolling(window=window).mean()
    rolling_std = data['Close'].rolling(window=window).std()
    upper_band = rolling_mean + (rolling_std * num_std)
    lower_band = rolling_mean - (rolling_std * num_std)
    return rolling_mean, upper_band, lower_band

# Function to calculate RSI
def calculate_rsi(data, window):
    delta = data['Close'].diff()
    up, down = delta.copy(), delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0
    roll_up = up.rolling(window=window).mean()
    roll_down = down.rolling(window=window).mean().abs()
    rs = roll_up / roll_down
    rsi = 100.0 - (100.0 / (1.0 + rs))
    return rsi

# Function to plot stock data
def plot_stock_data(data, ticker):
    data_mpf = data.set_index('Date')
    
    # Candlestick chart
    mpf.plot(data_mpf, type='candle', style='charles', title=f'{ticker} Stock Price', ylabel='Price', volume=False)
    
    # Moving Average and Bollinger Bands
    ap = [
        mpf.make_addplot(data['20_MA'], color='orange'),
        mpf.make_addplot(data['Upper_Band'], color='green'),
        mpf.make_addplot(data['Lower_Band'], color='red'),
    ]
    mpf.plot(data_mpf, type='candle', addplot=ap, title=f'{ticker} Moving Average and Bollinger Bands', ylabel='Price', volume=False)

    # Plot RSI
    plt.figure(figsize=(12, 6))
    plt.plot(data['RSI'], label='RSI', color='purple')
    plt.axhline(70, linestyle='--', alpha=0.5, color='red')
    plt.axhline(30, linestyle='--', alpha=0.5, color='green')
    plt.title(f'{ticker} RSI')
    plt.ylabel('RSI')
    plt.legend()
    plt.grid(True)

# Real-time update function
def update(frame, ticker):
    plt.clf()  # Clear current figure
    data = fetch_stock_data(ticker, '2023-01-01', '2023-09-01')
    data.reset_index(inplace=True)
    data['20_MA'] = calculate_moving_average(data, 20)
    data['Upper_Band'], data['Middle_Band'], data['Lower_Band'] = calculate_bollinger_bands(data, 20, 2)
    data['RSI'] = calculate_rsi(data, 14)
    
    plot_stock_data(data, ticker)
    plt.show()

# Main execution
ticker = 'AAPL'

# Animation setup
fig = plt.figure(figsize=(12, 6))
ani = FuncAnimation(fig, update, fargs=(ticker,), interval=60000)  # Update every minute

plt.show()
