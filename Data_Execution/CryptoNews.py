import requests
import json
import feedparser #RSS'lere bağlanarak websitelerinden scrape yapmaya olanak sağlayan 3rd party Python kütüphanesi. "pip" komutuyla yükledim.
from bs4 import BeautifulSoup #html içeriği çektiğim vakit tüm html kodlarını silip sadece text'i tutan bir kütüphane.

#Kripto haberleri yapan sitelerin RSS'inin linklerini koyduğum dictionary
Website_RSS = {
    "CoinDesk": "https://www.coindesk.com/arc/outboundfeeds/rss/?outputType=xml",
    "Cointelegraph": "https://cointelegraph.com/rss",
    "CryptoSlate": "https://cryptoslate.com/feed/",
    "The Defiant": "https://thedefiant.io/feed/",
}

News_Feed = []
raw_html = []


def get_cryptonews():

    for website, rss_url in Website_RSS.items(): #items metodu ile Website_RSS kütüphanesindeki key ve value dönüşünü yapabiliyorum --> (key, value) --> (CoinDesk, http//:....)

        #print(type(feed)) abd print(feed.key) yazdığımda feedparser kütüphanesi şu şekilde dönüyor: dict_keys(['feed', 'entries', 'bozo', 'headers', ...])
        #feedparser'ın yarattığım dictionary'deki keyleri dönebilmesi için ilgili keyleri ilerleyen aşamalarda referans vermem gerekiyor.
        feed = feedparser.parse(rss_url) 

        for entry in feed.entries[:5]: #Her bir websitesi için 5 tane çıktı dönsün sonra artırırım.

            #Eğer RSS, content yani makale için dönüş yapıyorsa raw_html değişkenine atıyorum. Eğer dönüş olmuyorsa genelde dönüş sağladıkları özet yani "summary" key'ini atıyorum.
            if "content" in entry and entry.content:
                raw_html = entry.content[0].value #entry.content bir list. .value ile HTML'in body'sini çekiyorum.
            else:
                raw_html = entry.get("summary", "")

            # Clean HTML → text
            clean_text = BeautifulSoup(raw_html, "html.parser").get_text(separator=" ", strip=True)

            News_Feed.append({
                "Source": website,
                "Title": entry.get("title", ""),
                "Published": entry.get("published", entry.get("updated", "")),
                #"link": entry.get("link", ""),
                "Content": clean_text
            })
        
    return News_Feed 

#print(json.dumps(News_Feed, indent=2))






