import requests
import json
import time
from Modules.Dominance import get_btc_dominance
from Modules.CryptoNews import get_cryptonews
from Modules.FundRate_V2 import get_fundrate
from Modules.OrderBook import get_order_book, get_orderbook_list
from Modules.Pricing import get_pricing
from Modules.Volume import get_volume

from Agents.dom_agent import analyze_btc_dom
from Agents.fund_agent import analyze_fundrate
from Agents.orderbook_agent import analyze_orderbook
from Agents.pricing_agent import analyze_pricing
from Agents.volume_agent import analyze_volume
from Agents.prediction_agent import pump_prediction

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


#1) BTC dominance analizi yapan agent
btc_dom = get_btc_dominance()
current_dom = analyze_btc_dom(btc_dom)
time.sleep(5.0)

#2) Fiyat analizi yapan agent
current_price_data, price_history_data = get_pricing()
pricing_analysis = analyze_pricing(current_price_data, price_history_data)
time.sleep(5.0)

#3) Fundrate analizi yapan agent
fundrate = get_fundrate()
fundrate_analysis = analyze_fundrate(fundrate)
time.sleep(5.0)

#4) Ask ve Bid analizi yapan order Book Agent
orderbook = get_orderbook_list(Crypto_Types)
orderbook_analysis = analyze_orderbook(orderbook)
time.sleep(5.0)

#5) Volume analizi yapan agent
volume = get_volume()
volume_analysis = analyze_volume(volume)
time.sleep(5.0)

final_result = pump_prediction(
        btc_dom_analysis = current_dom,
        funding_analysis = fundrate_analysis,
        orderbook_analysis =orderbook_analysis,
        pricing_analysis = pricing_analysis,
        volume_analysis = volume_analysis
    )

print("\n==============================")
print(" FINAL MARKET REPORT")
print("==============================")
print(final_result["report"]["market_read"])

print("\n--- PREDICTIONS ---")
print("6H :", final_result["predictions"]["6H"])
print("1D :", final_result["predictions"]["1D"])
print("7D :", final_result["predictions"]["7D"])

