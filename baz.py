import requests
import json

apiKey = "8b47b741-8018-4ea2-a564-b01d5302b1d6"
l = "api.hypixel.net/skyblock/bazaar/products?key=8b47b741-8018-4ea2-a564-b01d5302b1d6"


def get_products():
    items = ['COBBLESTONE','ENCHANTED_COBBLESTONE','ENCHANTED_MELON_BLOCK','ENCHANTED_MELON',
         'ENCHANTED_POTATO','','ENCHANTED_PUMPKIN','STRING','ENCHANTED_STRING',]
    url = "https://api.hypixel.net/v2/skyblock/bazaar"
    response = requests.get(url)
    data = response.json()
    for product in data['products']:
        if 'sell_summary' in data['products'][product]:
            del data['products'][product]['sell_summary']
        if 'buy_summary' in data['products'][product]:
            del data['products'][product]['buy_summary']
        

    ##with open('data.json', 'w') as f:
        ##json.dump(data, f)

    
        
    return data

def calculate_price(data):
    itemsb160 = ['IRON_INGOT','MELON','DIAMOND']
    itemse160 = ['ENCHANTED_IRON','ENCHANTED_MELON','ENCHANTED_DIAMOND']
    items8= []

    for item in itemsb160:
        sell_price = data['products'][item]['quick_status']['sellPrice']
        rounded_sell_price = round(sell_price,1)
        price = rounded_sell_price * 160
        print(item+": " + str(price))
        




if __name__ == "__main__":
    calculate_price(get_products())