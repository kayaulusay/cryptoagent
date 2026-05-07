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

#ask ve bid verisini çeken fonksiyon tanımlandı.
#symbol ile coin tipini çekiyorum
#limit ile ask ve bid verisini oluşturan 1000 tane veriyi çekiyorum.
#band_percentage ile as ve bid emirlerinin 1%'lik kısmını alıyorum. Ask ve bid mantığında piyasa alışkanlığı genelde kısa vadeli hesaplar için 1% civarı olduğu için bu rakamı aldım.

def get_order_book(symbol, limit=200, band_percentage=0.01):

    url = "https://api.binance.com/api/v3/depth" #depth uzantısı, Binance endpointinden ask ve bid detaylarını dönüyor.

    #order_book kütüphanesi Binance'ten çektiğim ask ve bidleri doldurduğum kütüphane
    order_book = requests.get(url, params={"symbol": symbol, "limit": limit}, timeout=20).json()


    #Binance'ten gelen veriler string formatında. Basit matematik işlemi yapmam gerektiği için bu stringleri rakama çevirmem gerekiyor.
    #bids alım emirleri listesi. asks satış emirleri listesi.
    #bids, Binance'ten şu şekilde dönüyor bids = [{price, quantity}, {price, quantity}, ......] --> tuple listesi
    #float operasyonu ile stringi rakama çeviriyorum. Bunu liste içindeki bir for loop ile tüm veriler için yapıyorum.
    #***ÖNEMLİ***: Binance, verileri "bids" ve "ask" olarak dönüyor. Bu yüzden order_book["bids"] ile bu verileri alıp bids listesinin içine atıyorum.
    bids = [(float(price), float(quantity)) for price, quantity in order_book["bids"]]
    asks = [(float(price), float(quantity)) for price, quantity in order_book["asks"]]

    #bids[0] ile listedeki ilk tuple'ı çekiyorum. Binance, depth end pointinde ilk başa en yüksek bid'i koyuyor. [0] -> (100, 5)
    #bid[0][0]'da ilk tuple'ın ilk değerini çekiyorum. [0][0] -> (100)
    #Aynısını ask için yapıyorum. 

    best_bid = bids[0][0] #En yüksek alım fiyat emri
    best_ask = asks[0][0] #En düşük satış fiyat emri
    mid_level = (best_bid + best_ask) / 2 #Coin borsasında derinlik için önerilen ortalama fiyat. Fair Price diye geçiyor.

    bid_floor = mid_level * (1 - band_percentage) #bid_floor kaç çıkarsa bunun altındaki alım fiyatlarını görmezden geliyorum çünkü fiyat baskısı oluşturacak alana uzak.
    ask_ceil  = mid_level * (1 + band_percentage) #ask_ceil kaç çıkarsa bunun üstündeki satış fiyatlarını görmezden geliyorum çünkü fiyat baskısı oluşturacak alana uzak.


    #Yukarıkdai floor ve ceil belirlediğim alım ve satım fiyatlarının sınırlarına göre toplam talebi değişkenlere atıyorum.
    bid_qty_total = sum(quantity for price, quantity in bids if price >= bid_floor) 
    ask_qty_total = sum(quantity for price, quantity in asks if price <= ask_ceil)


    #***ÖNEMLİ***: return komutu olmazsa fonksiyondaki tüm veriler kaybolur. Hiçbir değişkende tutulmaz.
    return {
        "symbol": symbol,
        "mid_level": mid_level,
        "bid_qty_total": bid_qty_total,
        "ask_qty_total": ask_qty_total
    }

#get_orderbook fonksiyonundan tuple şeklinde gelen yapıyı, başka bir fonksiyonda for loop a sokup result dictionary'si içinde agent'a uygun hale getiriyorum.

def get_orderbook_list(symbols, limit=1000, band_percentage=0.01):
    results = []
    for sym in symbols:
        results.append(get_order_book(sym, limit=limit, band_percentage=band_percentage))
    return results

# for Coin in Crypto_Types:
#        data = get_order_book(symbol = Coin)
#        print(f"for {Coin},", f"mid price is {data["mid_level"]},", f"bid liquidity near price is {data["bid_qty_total"]},", f"and ask liquidity is {data["ask_qty_total"]}.")