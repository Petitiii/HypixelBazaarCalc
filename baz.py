import requests
import yaml
from colorama import Fore
from colorama import Style
import schedule
import time
from datetime import datetime


class Item:
    def __init__(self,id,sellP,buyP,timeStamp):
        self.productId= id
        self.sellPrice=buyP
        self.buyPrice=sellP
        self.timeStamp=timeStamp
        
ITEMS160 = ['IRON_INGOT','MELON','DIAMOND','GOLD_INGOT','EMERALD','SAND','OBSIDIAN','LEATHER','ENCHANTED_IRON_INGOT', 
            'ENCHANTED_MELON', 'ENCHANTED_DIAMOND', 'ENCHANTED_GOLD_INGOT', 'ENCHANTED_EMERALD', 'ENCHANTED_SAND', 'ENCHANTED_OBSIDIAN', 'ENCHANTED_LEATHER',
            'ENCHANTED_IRON_INGOT_BLOCK', 'ENCHANTED_MELON_BLOCK', 'ENCHANTED_DIAMOND_BLOCK', 'ENCHANTED_GOLD_INGOT_BLOCK', 'ENCHANTED_EMERALD_BLOCK', 'ENCHANTED_SAND_BLOCK',
            'ENCHANTED_OBSIDIAN_BLOCK', 'ENCHANTED_LEATHER_BLOCK']
DATA_FILE = 'data.yaml'


def get_products():
    itemsobjects = []
    itemsdict = {}
    url = "https://api.hypixel.net/v2/skyblock/bazaar"
    response = requests.get(url)
    data = response.json()
    for product in data['products']:
        if 'sell_summary' in data['products'][product]:
            del data['products'][product]['sell_summary']
        if 'buy_summary' in data['products'][product]:
            del data['products'][product]['buy_summary']
    
    for product in data['products']:
        if product not in ITEMS160:
            continue
        ##create new Item object
        timeStamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        item = Item(product,round(data['products'][product]['quick_status']['sellPrice'],1),round(data['products'][product]['quick_status']['buyPrice'],1),timeStamp)
        
        itemsobjects.append(item)

    
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

def saveCSV(data):
    with open('data.csv', 'a') as f:
        f.write("productId,sellPrice,buyPrice,timeStamp\n")
        for item in data:
            f.write(item.productId + "," + str(item.sellPrice) + "," + str(item.buyPrice) +","+ str(item.timeStamp)+"\n")
    
#def getInfo():
 #   with open(DATA_FILE) as f:
  #      file = yaml.load(f.read(), Loader=yaml.Loader)
   # return file

# TODO durchlaufen und appenden
#def printInfos(itemarray):
 #   with open(DATA_FILE, 'w') as f:
  #      yaml.dump(itemarray, f)
            
def job():
    data = get_products()
    calcute_price(data)
    
    

schedule.every(60).seconds.do(job)
        
    
    
if __name__ == "__main__":
    job()
    
    #printInfos(get_products())
    
    
    
    while True:
        schedule.run_pending()
        time.sleep(1)