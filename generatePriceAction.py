import random
import json
import matplotlib.pyplot as plt

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
    return prices, initial_price

# Generate price data for a crypto asset
num_days = 365  # Number of days
seed_value = 42  # Seed for replication
price_data, initial_price = generate_crypto_price_action(num_days, volatility=0.8, drift=0.15, seed=seed_value)

# Save price data to a JSON file along with initial price and seed for replication
data_to_save = {'seed': seed_value, 'initial_price': initial_price, 'prices': price_data}

with open('crypto_price_data.json', 'w') as json_file:
    json.dump(data_to_save, json_file)

# Plotting the price action for a crypto asset
plt.figure(figsize=(10, 6))
plt.plot(range(num_days), price_data, label='Price')
plt.title('Simulated Crypto Asset Price Action')
plt.xlabel('Days')
plt.ylabel('Price')
plt.legend()
plt.grid(True)
plt.show()
