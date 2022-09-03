# Zewen Lin
import time
import requests
from bs4 import BeautifulSoup

HEADERS = ({'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/100.0.4896.127 Safari/537.36'})

URL_DICT = {"Nikon Z5": ["https://www.bestbuy.com/site/nikon-z-5-camera-body-black/6423074.p?skuId=6423074",
                         "https://www.ebay.com/itm/393051368815?epid=23040179337&hash=item5b83afed6f:g:c18AAOSw629f0nlN"],
            "Xbox Series S(512GB)": ["https://www.bestbuy.com/site/microsoft-xbox-series-s-512-gb-all-digital-console"
                                     "-disc "
                                     "-free-gaming-white/6430277.p?skuId=6430277",
                                     "https://www.ebay.com/itm/265441750836?epid=8040996571&hash=item3dcd8faf34%3Ag"
                                     "%3ArwYAAOSwzIRhsA6Y&LH_BIN=1&LH_ItemCondition=1000"],
            "Ipad pro 11-inch": ["https://www.bestbuy.com/site/apple-11-inch-ipad-pro-latest-model-with-wi-fi-128gb"
                                 "-space-gray/4265400.p?skuId=4265400",
                                 "https://www.ebay.com/itm/274849279738?epid=5045915216&_trkparms=ispr%3D1&hash"
                                 "=item3ffe4b2efa%3Ag%3AXGcAAOSwlRBg2i5i&amdata=enc"
                                 "%3AAQAGAAAA4H9gUX63kuNvZ78M8tc24sqHaZ1vie6sJ9Rmjs0d0M6UHk9K%2B33l2iLg2SiBMstxT"
                                 "%2FnAMsnU8DwAtD8WqmQ%2FHeFeHvX2CqtGa7NE6U9GtIpTv01R5zxSl4lb3gH1Abuont31O9XpL"
                                 "%2B1efczoe3zgH0Bd4afVWPHf7rPIZA8pNWBiKRVRrUm2Hy9IxpzZWyn%2FANv"
                                 "%2BKEERrXPIhaZFkwq2wGYyU6aEpujXowKY9PU73Wd%2Fzza93PhoTEE9CTP"
                                 "%2BgIM6559B1hu9ZqsQmQ0W5ZHVrWkyIl8mh7kbTTSWjwYIcMdM%7Ctkp%3ABFBMmMX3oZBg&LH_BIN=1"
                                 "&LH_ItemCondition=1000"],
            "AirPods(3rd gen)": [
                "https://www.bestbuy.com/site/apple-airpods-3rd-generation-white/4900944.p?skuId=4900944",
                "https://www.ebay.com/itm/255471415645?epid=21050834847&_trkparms=ispr%3D5&hash"
                "=item3b7b48715d%3Ag%3ADdoAAOSwc4xiSygO&amdata=enc%3AAQAGAAAA0EqaoiDJyVBktCqHB%2B7TR"
                "%2FiZ4%2FPxBfXqYV1Dc0ftGwiHMfVnWL0fMx0Ct2eJt03moP%2B1AzfwwThTkMatHXmHT"
                "%2Fal9n3IIia7Nap%2FfrkpLZMDDC7Xcj1mLbC%2BxTaV3dOnvF372F64Oim5Yo2UrI"
                "%2BkowDQ8mjxKhzUro%2BFlQfeLUUHc%2B5%2BKY%2FhBImni"
                "%2F1xCiK1RtlUBxeYQ5PjhKBgeBdbe7dQhja6pXI%2Bhu%2FdBsYam0oFbz%2FrPVXAn1AL8UbgxOC"
                "%2FCn8BnsIpDBVU0TJVpUEhg8E%3D%7Ctkp%3ABlBMUJbWxqGQYA&LH_BIN=1&LH_ItemCondition=3"]}


class PriceTracker:
    def __init__(self, item_title):
        self.item_title = item_title

    def get_price_bestbuy(self, bestbuy_url):
        html = requests.get(bestbuy_url, headers=HEADERS)
        soup = BeautifulSoup(html.content, "html.parser")
        title = soup.find(class_="heading-5 v-fw-regular").text
        price = (soup.find(class_="sr-only").text.split())[-1]
        return title, price

    def get_price_ebay(self, ebay_url):
        html = requests.get(ebay_url, headers=HEADERS)
        soup = BeautifulSoup(html.content, "html.parser")
        title = soup.find(class_="x-item-title__mainTitle").text.strip()
        price = soup.find(id="prcIsum").text.strip()
        return title, price

    def run(self):
        bestbuy = self.get_price_bestbuy(URL_DICT[self.item_title][0])
        ebay = self.get_price_ebay(URL_DICT[self.item_title][1])
        return bestbuy, ebay


# priceTracker = PriceTracker("")
# priceTracker.run()
