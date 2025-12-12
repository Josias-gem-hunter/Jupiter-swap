import requests
import time
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# --- CONFIGURATION ---
API_URL = "https://freegoldapi.com/data/latest.json"  # Free endpoint
ALERT_PRICE = 2100  # Alert threshold
CHECK_INTERVAL = 3600  # seconds (1 hour)

# --- FUNCTIONS ---
def get_gold_price():
    response = requests.get(API_URL)
    data = response.json()
    # Assuming API returns latest price at index -1
    latest = data[-1]
    price = float(latest['price'])
    timestamp = latest['timestamp']
    return price, timestamp

def plot_prices(prices, timestamps):
    df = pd.DataFrame({'Price': prices}, index=pd.to_datetime(timestamps, unit='s'))
    df.plot(figsize=(10,5), title="Gold Price History")
    plt.xlabel("Time")
    plt.ylabel("Price (USD)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# --- MAIN LOOP ---
historical_prices = []
historical_timestamps = []

while True:
    price, timestamp = get_gold_price()
    print(f"Current Gold Price: ${price} at {datetime.fromtimestamp(timestamp)}")
    
    historical_prices.append(price)
    historical_timestamps.append(timestamp)

    if price > ALERT_PRICE:
        print(f"⚠️ ALERT! Gold price is above ${ALERT_PRICE}!")

    # Plot chart each time
    plot_prices(historical_prices, historical_timestamps)
    
    time.sleep(CHECK_INTERVAL)
