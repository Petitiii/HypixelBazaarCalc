import requests
import json

apiKey = "8b47b741-8018-4ea2-a564-b01d5302b1d6"
l = "api.hypixel.net/skyblock/bazaar/products?key=8b47b741-8018-4ea2-a564-b01d5302b1d6"


def get_products():
    url = "https://api.hypixel.net/v2/skyblock/bazaar"
    response = requests.get(url)
    data = response.json()
    with open('products.txt', 'w') as outfile:
        json.dump(data, outfile)
    return data

def get_moneyy():
    with open('products.txt', 'r') as f:
        for line in f:
            if 'specific_word' in line:  # replace 'specific_word' with the word you're looking for
                print(line)


if __name__ == "__main__":
    get_products()