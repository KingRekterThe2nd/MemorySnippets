import random
import json
import matplotlib.pyplot as plt

def calculate_sma(prices, window):
    sma_values = []
    for i in range(len(prices)):
        if i < window - 1:
            sma_values.append(None)
        else:
            sma = sum(prices[i - window + 1 : i + 1]) / window
            sma_values.append(sma)
    return sma_values

def calculate_ema(prices, window):
    ema_values = []
    multiplier = 2 / (window + 1)
    ema = sum(prices[:window]) / window
    ema_values.extend([None] * (window - 1))  # Adding None values for initial indices
    ema_values.append(ema)
    for i in range(window, len(prices)):
        ema = (prices[i] - ema) * multiplier + ema
        ema_values.append(ema)
    return ema_values

def calculate_rsi(prices, window=14):
    deltas = [prices[i + 1] - prices[i] for i in range(len(prices) - 1)]
    gains = [delta if delta > 0 else 0 for delta in deltas]
    losses = [abs(delta) if delta < 0 else 0 for delta in deltas]
    
    avg_gain = sum(gains[:window]) / window
    avg_loss = sum(losses[:window]) / window

    rs = avg_gain / avg_loss if avg_loss != 0 else 0
    rsi_values = [None] 

    for i in range(0, len(prices) - 1):
        delta = prices[i + 1] - prices[i]
        gain = delta if delta > 0 else 0
        loss = abs(delta) if delta < 0 else 0
        avg_gain = (avg_gain * (window - 1) + gain) / window
        avg_loss = (avg_loss * (window - 1) + loss) / window
        rs = avg_gain / avg_loss if avg_loss != 0 else 0
        rsi = 100 - (100 / (1 + rs))
        rsi_values.append(rsi)
    
    return rsi_values


def generate_crypto_price_action(days, volatility=0.5, drift=0.1, seed=None):
    if seed is not None:
        random.seed(seed)
    initial_price = random.uniform(100, 1000)  # Random initial price between 100 and 1000
    prices = [initial_price]
    for day in range(1, days):
        daily_drift = drift / 365  # Assuming 365 days in a year
        shock = random.normalvariate(0, 1) * volatility / (365 ** 0.5)
        price = prices[-1] * (1 + daily_drift + shock)
        prices.append(price)
    
    sma_20 = calculate_sma(prices, 20)
    ema_50 = calculate_ema(prices, 50)
    rsi_14 = calculate_rsi(prices)
    
    return prices, initial_price, sma_20, ema_50, rsi_14

# Generate price data for a crypto asset
num_days = 365  # Number of days
seed_value = 42  # Seed for replication
price_data, initial_price, sma_20, ema_50, rsi_14 = generate_crypto_price_action(num_days, volatility=0.8, drift=0.15, seed=seed_value)

# Save price data and indicators to a JSON file along with initial price and seed for replication
data_to_save = {
    'seed': seed_value,
    'initial_price': initial_price,
    'prices': price_data,
    'sma_20': sma_20,
    'ema_50': ema_50, 
    'rsi_14': rsi_14
}

with open(f'crypto_price_data_{seed_value}.json', 'w') as json_file:
    json.dump(data_to_save, json_file)

# Plotting the price action for a crypto asset along with indicators
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), gridspec_kw={'height_ratios': [3, 1]})
ax1.plot(range(0,len(price_data)), price_data, label='Price',color='black')
ax1.plot(range(0,len(price_data)), sma_20, label='SMA (20)', color='orange')
ax1.plot(range(0,len(price_data)), ema_50, label='EMA (50)',color='blue')
ax1.set_title('Simulated Crypto Asset Price Action with SMA (20)')
ax1.set_ylabel('Price')
ax1.legend()
ax1.grid(axis='y')  # Horizontal grid lines only
ax1.xaxis.grid(False)  # Disable vertical grid lines

ax2.plot(range(0,len(price_data)), rsi_14, label='RSI (14)',color='black')
ax2.set_title('RSI (14)')
ax2.set_xlabel('Days')
ax2.set_ylabel('RSI Value')
ax2.legend()
ax2.grid(axis='y')  # Horizontal grid lines only
ax2.xaxis.grid(False)  # Disable vertical grid lines

plt.tight_layout()
plt.show()
