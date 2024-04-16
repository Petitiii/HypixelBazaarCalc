import requests
import json
from colorama import Fore
from colorama import Style
import schedule
import time

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
                    profitPercentage = round((profit / item2.buyPrice)*100)

                    if profitPercentage < 10:
                        color = Fore.RED
                    elif profitPercentage > 25:
                        color = Fore.GREEN
                    elif profitPercentage > 50:
                        color = Fore.GREEN
                    else:
                        color = Fore.RESET

                    if profitflipitem1 < 2:
                        colorf1 = Fore.RED
                    elif profitflipitem1 > 10:
                        colorf1 = Fore.GREEN
                    else:
                        colorf1 = Fore.RESET

                    if profitflipitem2 < 2:
                        colorf2 = Fore.RED
                    elif profitflipitem2 > 10:
                        colorf2 = Fore.GREEN
                    else:
                        colorf2 = Fore.RESET
                    colorS = Fore.RESET


                    print(colorS+Style.BRIGHT + item.productId + Style.RESET_ALL + "\nS: " + str(round(item.sellPrice, 1)) + " Coins B: " + str(round(item.buyPrice, 1)) + " Coins")
                    print(colorf1+"Flip: "+str(flipitem1) +" Coins "+str(profitflipitem1)+"%")
                    print(colorS+Style.BRIGHT + item2.productId + Style.RESET_ALL + "\nS: " + str(round(item2.sellPrice, 1)) + " Coins B: " + str(round(item2.buyPrice, 1)) + " Coins")
                    print(color + "Craftprofit: " + str(profit)+ " Coins", str(profitPercentage) + "%" + Fore.RESET)
                    print(colorf2+"Flip: "+str(flipitem2) +" Coins "+str(profitflipitem2)+"%")
                    
                    for item3 in itemarray:
                        if item3.productId == item2.productId+ '_BLOCK':

                            flipitem3 = round(item3.sellPrice - item3.buyPrice,1)
                            profitflipitem3= round(((item3.sellPrice - item3.buyPrice)/item3.sellPrice)*100,1)
                            profit = round(item3.sellPrice - item2.buyPrice*160,1)
                            profitPercentage = round(((item3.buyPrice - item3.buyPrice)/item3.sellPrice)*100)

                            if profitPercentage < 10:
                                color = Fore.RED
                            elif profitPercentage > 25:
                                color = Fore.GREEN
                            elif profitPercentage > 50:
                                color = Fore.GREEN
                            else:
                                color = Fore.RESET

                            if profitflipitem3 < 2:
                                colorf = Fore.RED
                            elif profitflipitem3 > 10:
                                colorf = Fore.GREEN
                            else:
                                colorf = Fore.RESET

                            
                            print(colorS+Style.BRIGHT + item3.productId + Style.RESET_ALL +"\nS: " + str(round(item3.sellPrice, 1)) + " Coins B: " + str(round(item3.buyPrice, 1)) + " Coins")
                            print(color + "Craftprofit: " + str(profit)+ " Coins", str(profitPercentage) + "%" + Fore.RESET)
                            print(colorf+"Flip: "+str(flipitem3) +" Coins "+str(profitflipitem3)+"%")

def printInfos(itemarray):
    with open('data.txt', 'w') as f:
        for item in itemarray:
            f.write(item.productId + "\n")
            
def job():
        calcute_price(get_products())
    

schedule.every(15).seconds.do(job)
        
    
    
if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)