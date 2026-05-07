import requests  #Python kütüphanesinden HTTP requestlerine call atmak için kullandım.
import json  #JSON modülünü kullanım için yükler.
from requests.adapters import HTTPAdapter #Her bir seassion'ı kontrol eden Python adaptörü.
from urllib3.util.retry import Retry #Eğer API call patlarsa tekrar "reques" atmasını sağayan kütüphane.

#Funding Rate değerlerini öğrenmek istediğim kripto paraların Binance'teki sembollerini bir listede tutuyorum.
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

#Binance'in tüm sembollere one time API call sağlayan uzantısı. Böylece tüm coinler için listedeki coin sayısı kadar request atmamış oluyorum.
funding_url = "https://fapi.binance.com/fapi/v1/premiumIndex"



def _session() -> requests.Session: #session tutması ve retry operasyonlarını yönetebilmesi için bir fonksiyon
    s = requests.Session() #sessionları tutan object
    retry = Retry(
        total=5, #en fazla 5 tane retry yap. 5'ten fazla fail olursa dur.
        backoff_factor=0.5, #her bir retry arasında 0,5 saniye bekle.
        status_forcelist=(429, 500, 502, 503, 504), #farklı kanallara retry atarak yoğunluğu azaltıyor.
        allowed_methods=("GET",),
        raise_on_status=False,
    )
    s.mount("https://", HTTPAdapter(max_retries=retry)) #retry adaptörünü ekliyorum.
    return s


def get_fundrate():

    wanted = set(Crypto_Types)
    s = _session()

    request = s.get(funding_url, timeout=(3, 10)) #binance'e gönderilecek request. 3 saniye civarı bağlantı, 10 saniye civarı da download.
    request.raise_for_status()
    data = request.json()

    funding_data = {}
    for item in data:
        sym = item.get("symbol")
        if sym in wanted:
            funding_data[sym] = {
                "fundingRate": float(item["lastFundingRate"]),
                "nextFundingTime": int(item["nextFundingTime"]),
            }

    return funding_data

# result = get_fundrate()
# print(result)

# def get_fundrate():

#     funding_data = [] #coin verilerinin saklanması için boş bir list (array) tanımladım.

#     #Crypto_Types listesindeki tüm coinlere tek tek bakıp ekrana bastırmak için for loop
#     for Coin in Crypto_Types:

#         #funding değişkenine request kütüphanesindeki get metodu ile istek yolluyorum.
#         #params değişkeni, Binance'in zorunlu tuttuğu bir değişken. Binance tarafında https://fapi.binance.com/fapi/v1/fundingRate?symbol=BTCUSDT&limit=1 şeklinde bir quesry yaratıyor.
#         #symbol, Binance'in scrape için zorunlu tuttuğu bir dictionary. Crypto_Types listesi içindeki değer (value), symbol key'inin içien geliyor.
#         #limit key'i ise Binance'deki en güncel funding rate değerine bakıyor.
#         #En sondaki .json(), Binance'deki json formatındaki veriyi Python'a Python objesi olarak gönderiyor.
#         funding = requests.get(funding_url, params = {"symbol": Coin, "limit": 1}).json()


#         #for loop'ta her bir coin Binance'ten döndüğü vakit funding_data dictionary'sine ekleniyor. Bunu yapmazsam funding değişkeninde sadece en son çekilen coin verisi kalır.
#         funding_data.append({"symbol": Coin, "data": funding})
    
#     return funding_data

# result = get_fundrate()
# print(result)