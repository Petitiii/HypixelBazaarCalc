import requests
import json
from colorama import Fore

apiKey = "8b47b741-8018-4ea2-a564-b01d5302b1d6"
l = "api.hypixel.net/skyblock/bazaar/products?key=8b47b741-8018-4ea2-a564-b01d5302b1d6"

class Item:
    def __init__(self,id,sellP,buyP):
        self.productId= id
        self.sellPrice=buyP
        self.buyPrice=sellP
        



def get_products():
    itemsobjects = []
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
    
    for product in data['products']:
        ##create new Item object
        item = Item(product,data['products'][product]['quick_status']['sellPrice'],data['products'][product]['quick_status']['buyPrice'])
        itemsobjects.append(item)
        ##with open('data.json', 'w') as f:
        ##json.dump(data, f)
    
    return itemsobjects

        
def calcute_price(itemarray):
    itemsb160 = ['IRON_INGOT','MELON','DIAMOND','GOLD_INGOT','EMERALD','SAND','OBSIDIAN','LEATHER']
    for item in itemarray:
        if item.productId in itemsb160:
            for item2 in itemarray:
                if item2.productId == 'ENCHANTED_'+item.productId: 
                    
                    flipitem1 = round(item.sellPrice - item.buyPrice,1)
                    profitflipitem1= round((flipitem1/item.sellPrice*100))

                    flipitem2 = round(item2.sellPrice - item2.buyPrice,1)
                    profitflipitem2= round((flipitem2/item2.sellPrice*100))

                    profit = round(item2.sellPrice - item.buyPrice*160,1)
                    profitPercentage = round((profit / item2.sellPrice)*100)

                    if profitPercentage < 10:
                        color = Fore.RED
                    elif profitPercentage > 25:
                        color = Fore.GREEN
                    elif profitPercentage > 50:
                        color = Fore.GREEN
                    else:
                        color = Fore.RESET

                    print(item.productId + "\nS: " + str(round(item.sellPrice, 1)) + " Coins B: " + str(round(item.buyPrice, 1)) + " Coins")
                    print("Flip: "+str(flipitem1) +" Coins "+str(profitflipitem1)+"%")
                    print(item2.productId + "\nS: " + str(round(item2.sellPrice, 1)) + " Coins B: " + str(round(item2.buyPrice, 1)) + " Coins")
                    print(color + "CraftProfit: " + str(profit)+ " Coins", str(profitPercentage) + "%" + Fore.RESET)
                    print("Flip: "+str(flipitem2) +" Coins "+str(profitflipitem2)+"%")
                    
                    for item3 in itemarray:
                        if item3.productId == item2.productId+ '_BLOCK':

                            flipitem3 = round(item3.sellPrice - item3.buyPrice,1)
                            profitflipitem3= round((flipitem3/item.sellPrice*100))
                            profit = round(item3.sellPrice - item2.buyPrice*160,1)
                            profitPercentage = round((profit / item3.sellPrice)*100)



                            if profitPercentage < 10:
                                color = Fore.RED
                            elif profitPercentage > 25:
                                color = Fore.GREEN
                            elif profitPercentage > 50:
                                color = Fore.GREEN
                            else:
                                color = Fore.RESET

                            
                            print(item3.productId +"\nS: " + str(round(item3.sellPrice, 1)) + " Coins B: " + str(round(item3.buyPrice, 1)) + " Coins")
                            print(color + "Craft Profit: " + str(profit)+ " Coins", str(profitPercentage) + "%" + Fore.RESET)
                            print("Flip: "+str(flipitem3) +" Coins "+str(profitflipitem3)+"%")
                    
                    
                
               
        
            
            




def calculate_price1(data):
    itemsb160 = ['IRON_INGOT','MELON','DIAMOND','GOLD_INGOT','EMERALD','SAND','OBSIDIAN','LEATHER']
    itemse160 = ['ENCHANTED_IRON','ENCHANTED_MELON','ENCHANTED_DIAMOND']
    items8= []

    for item in itemsb160:
        sell_price = data['products'][item]['quick_status']['sellPrice']
        rounded_sell_price = round(sell_price,1)
        price = rounded_sell_price * 160
        print(item+": " + str(price))



if __name__ == "__main__":
    calcute_price(get_products())