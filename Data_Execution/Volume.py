import requests
import json

#Binance API'sinin symbol yapısına göre liste oluşturuldu.
Crypto_Types = [
    "BTCUSDT",
    "ETHUSDT",
    "SOLUSDT",
    "XRPUSDT",
    "ADAUSDT",
    "DOGEUSDT",
    "AVAXUSDT",
    "PEPEUSDT",
    "FLOKIUSDT",
    "API3USDT",
    "WLFIUSDT",
    "TIAUSDT",
    "EIGENUSDT",
    "ALICEUSDT",  
    "ZRXUSDT",
    "APTUSDT",
    "BONKUSDT",
    "GLMUSDT",
    "ETHFIUSDT",
    "WIFUSDT",
    "AUDIOUSDT",   
] 


def get_volume():
    volume_result = []

    for Coin in Crypto_Types:

        url = "https://api.binance.com/api/v3/ticker/24hr"
        total_data = requests.get(url, params={"symbol": Coin}).json()

        volume_result.append({
            "coin": Coin,
            "current_volume": total_data
        })

    return volume_result

result = get_volume()
print(result)