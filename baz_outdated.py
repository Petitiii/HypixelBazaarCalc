import requests
from datetime import datetime
import time

def get_products():
    try:
        url = "https://api.hypixel.net/v2/skyblock/bazaar"
        response = requests.get(url)
        data = response.json()

        # Get the current timestamp and format it to "YYYY-MM-DD HH:MM"
        current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')

        allowed_items = [
            "DIAMOND", "ENCHANTED_DIAMOND", "ENCHANTED_DIAMOND_BLOCK",
            "COBBLESTONE", "ENCHANTED_COBBLESTONE", "COAL", "ENCHANTED_COAL",
            "ENCHANTED_COAL_BLOCK", "BAZAAR_COOKIE", "MELON", "ENCHANTED_MELON",
            "ENCHANTED_MELON_BLOCK", "ENCHANTED_GLISTERING_MELON", "WHEAT", 
            "ENCHANTED_BREAD", "ENCHANTED_HAY_BLOCK", "MITHRIL_ORE", "ENCHANTED_MITHRIL",
            "ENCHANTED_LAPIS_LAZULI", "ENCHANTED_LAPIS_LAZULI_BLOCK", "ENCHANTED_CACTUS_GREEN",
            "ENCHANTED_PACKED_ICE", "ICE_BAIT", "WHALE_BAIT"
        ]

        product_data = {}

        for product_id, product_data_entry in data['products'].items():
            if product_id not in allowed_items:
                continue

            quick_status = product_data_entry.get('quick_status', {})
            if not quick_status:
                continue

            # Extract quick_status fields
            sell_price = round(quick_status.get('sellPrice', 0), 1)
            buy_price = round(quick_status.get('buyPrice', 0), 1)
            sell_volume = round(quick_status.get('sellVolume', 0))
            buy_volume = round(quick_status.get('buyVolume', 0))
            sell_orders = round(quick_status.get('sellOrders', 0))
            buy_orders = round(quick_status.get('buyOrders', 0))

            # Aggregate product data
            product_data[product_id] = {
                'sell_price': sell_price,
                'buy_price': buy_price,
                'sell_volume': sell_volume,
                'buy_volume': buy_volume,
                'sell_orders': sell_orders,
                'buy_orders': buy_orders,
                'timestamp': current_timestamp
            }

        # Open a file in append mode
        with open('bazaar_data.txt', 'a') as file:
            for product_id, aggregated_data in product_data.items():
                # Write formatted data into the text file
                file.write(f"Product: {product_id}\n")
                file.write(f"Sell Price: {aggregated_data['sell_price']}\n")
                file.write(f"Buy Price: {aggregated_data['buy_price']}\n")
                file.write(f"Sell Volume: {aggregated_data['sell_volume']}\n")
                file.write(f"Buy Volume: {aggregated_data['buy_volume']}\n")
                file.write(f"Sell Orders: {aggregated_data['sell_orders']}\n")
                file.write(f"Buy Orders: {aggregated_data['buy_orders']}\n")
                file.write(f"Timestamp: {aggregated_data['timestamp']}\n")
                file.write("-" * 40 + "\n")  # Separator between products

        print(f"Data written to bazaar_data.txt at {current_timestamp}")

    except Exception as e:
        print(f"Error: {e}")

# Infinite loop to run the function every minute
while True:
    get_products()
    time.sleep(120)  # Wait for 120 seconds before running again