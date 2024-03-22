import requests
import json

apiKey = "8b47b741-8018-4ea2-a564-b01d5302b1d6"
l = "api.hypixel.net/skyblock/bazaar/products?key=8b47b741-8018-4ea2-a564-b01d5302b1d6"


def get_products():
    items = ['INK_SACK:3','COBBLESTONE','ENCHANTED_MELON_BLOCK','ENCHANTED_MELON','ENCHANTED_POTATO',
         'ENCHANTED_POTATO','ENCHANTED_PUMPKIN','ENCHANTED_PUMPKIN','ENCHANTED_SUGAR_CANE','ENCHANTED_SUGAR_CANE',
         'ENCHANTED_STRING','ENCHANTED_STRING']
    url = "https://api.hypixel.net/v2/skyblock/bazaar"
    response = requests.get(url)
    data = response.json()
    for item in items:
        print(item)
        sell_price = data['products'][item]['quick_status']['sellPrice']
        rounded_sell_price = round(sell_price,1)
        print(rounded_sell_price)
        
    return data




if __name__ == "__main__":
    get_products()