import requests
from datetime import datetime
import time
import psycopg2

# PostgreSQL database connection configuration
db_config = {
    'host': 'localhost',
    'dbname': 'SkyBlock',
    'user': '',
    'password': ''
}

def get_products():
    try:
        # Connect to PostgreSQL database
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        url = "https://api.hypixel.net/v2/skyblock/bazaar"
        response = requests.get(url)
        data = response.json()

        # Get the current timestamp
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

            # Insert product_id into items table (if not exists) and get product_key
            cursor.execute("""
                INSERT INTO items (product_id) 
                VALUES (%s) 
                ON CONFLICT (product_id) DO NOTHING
                RETURNING product_key;
            """, (product_id,))
            
            # If no new row is inserted, retrieve the product_key of the existing row
            product_key = cursor.fetchone()
            if product_key is None:
                cursor.execute("SELECT product_key FROM items WHERE product_id = %s;", (product_id,))
                product_key = cursor.fetchone()[0]

            # Insert into prices table with conflict handling
            cursor.execute("""
                INSERT INTO prices (product_key, sell_price, buy_price, timestamp) 
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (product_key, timestamp) DO UPDATE 
                SET sell_price = EXCLUDED.sell_price, buy_price = EXCLUDED.buy_price;
            """, (product_key, sell_price, buy_price, current_timestamp))

            # Insert into volumes table with conflict handling
            cursor.execute("""
                INSERT INTO volumes (product_key, sell_volume, buy_volume, timestamp) 
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (product_key, timestamp) DO UPDATE 
                SET sell_volume = EXCLUDED.sell_volume, buy_volume = EXCLUDED.buy_volume;
            """, (product_key, sell_volume, buy_volume, current_timestamp))

            # Insert into orders table with conflict handling
            cursor.execute("""
                INSERT INTO orders (product_key, sell_orders, buy_orders, timestamp) 
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (product_key, timestamp) DO UPDATE 
                SET sell_orders = EXCLUDED.sell_orders, buy_orders = EXCLUDED.buy_orders;
            """, (product_key, sell_orders, buy_orders, current_timestamp))

        # Commit the transaction
        conn.commit()

        
        cursor.close()
        conn.close()

        print(f"Data inserted into database at {current_timestamp}")

    except Exception as e:
        print(f"Error: {e}")


while True:
    get_products()
    time.sleep(600)  
