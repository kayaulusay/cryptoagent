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

current_price_url = "https://api.binance.com/api/v3/ticker/price"
#Güncel coin fiyat verilerinin saklanması için boş bir list (array) tanımladım.

price_history_url = "https://api.binance.com/api/v3/klines"
price_history_data = [] #önceki dönemlere ait coin fiyat verilerinin saklanması için boş bir list (array) tanımladım.

def get_pricing():

    current_price_data = []
    price_history_data = []

    for Coin in Crypto_Types:

        price = requests.get(current_price_url, params = {"symbol": Coin}).json()

        current_price = {"Coin Name": price["symbol"], "Current Price": price["price"]}

        #for loop'ta her bir coin Binance'den döndüğü vakit current_price_data dictionary'sine ekleniyor. Bunu yapmazsam fiyat değişkeninde sadece en son çekilen coin verisi kalır.
        current_price_data.append(current_price)

    current_price_text = json.dumps(current_price_data, indent=2) #indent değişkeni json formatını daha okunaklı hale getiriyor. Zorunlu değil.

    #print(current_price_text)

    TimeLine = [7, 30, 90, 365]

    for Coin in Crypto_Types:

        coin_record = {"Coin Name": Coin, "prices": {}} #İlgili coini buluyor. prices key'i ile tüm fiyatları nested loop'tan tek tek ekliyor.

        for days in TimeLine:

            #interval 1d seçildiği vakit Binance'ten günlük veriyi çekiyor
            #En güncel fiyatın zamanı 0'dan başlıyor. Bu yüzden Binance'ten gelen indeksi 7. gün ya da 365. günde çekebilmek için +1 koymak gerekiyor.
            days_data = requests.get(price_history_url, params = {"symbol": Coin, "interval": "1d", "limit": days+1}).json()

            final_price = float(days_data[0][4])
            coin_record["prices"][f"price before {days} days"] = final_price #Günle ilişkili fiyatı çekiyor. 7. ya da 30. günde fiyat ne ise onu days kısına getiriyor.


        price_history_data.append(coin_record) #Tüm fiyatları listeye ekliyorum.

    return current_price_data, price_history_data

if __name__ == "__main__":
    current_price_data, price_history_data = get_pricing()

    print("\n================ CURRENT PRICES ================\n")
    print(json.dumps(current_price_data, indent=2))

    print("\n================ PRICE HISTORY ================\n")
    print(json.dumps(price_history_data, indent=2))

# print(json.dumps(price_history_data, indent=2))