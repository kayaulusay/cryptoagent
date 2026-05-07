import requests
import json

btc_dom_data = []

def get_btc_dominance():



    dominance_url = "https://api.coingecko.com/api/v3/global"

    dom_data = requests.get(dominance_url).json()
    btc_dom_data = dom_data["data"]["market_cap_percentage"]["btc"]

    return btc_dom_data

#btc_dom = get_btc_dominance()
#print(f"BTC Dominance: {btc_dom:.1f}%")

#print(f"BTC Dominance: {btc_dom_data:.1f}%")