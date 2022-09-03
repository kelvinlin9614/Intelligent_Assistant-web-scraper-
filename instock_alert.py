import os

from selenium import webdriver as wd
from selenium.webdriver.common.by import By
import chromedriver_binary
from bs4 import BeautifulSoup
import time
import pandas as pd
import pywhatkit as kit

URL = "https://www.amazon.com/s?k=rtx+3080&sprefix=rtx+%2Caps%2C173&ref=nb_sb_ss_ts-doa-p_1_4"


class InStockAlert:
    def __init__(self, zipcode, maxPrice, webdriver, phoneNum, keyword, item_url=URL):
        self.zipcode = zipcode
        self.maxPrice = maxPrice
        self.wd = webdriver
        self.phoneNum = phoneNum
        self.keyword = keyword
        self.item_url = item_url

    # return a panda dataframe that contains the item title, sponsored, price, url
    def getPandaResult(self, searchResults):
        rows = []
        for result in searchResults:
            title = result.find("span", class_="a-text-normal")
            sponsored = result.find("span", class_="a-color-base", text="Sponsored")
            price = result.find("span", class_="a-price-whole")
            url = result.find("a", class_="a-link-normal")
            if price:
                format_price = str(price.text).replace(",", "")
                row = [title.text, bool(sponsored), format_price, "https://amazon.com/" + url['href']]
            rows.append(row)
        df = pd.DataFrame.from_records(rows, columns=["Title", "Sponsored", "Price", "URL"])
        return df

    # send message to whatsApp, the msg will contain a screenshot and a url
    # It will save the screenshot to local, and once sent the msg, It will delete the image
    def sendWhatsAppMsg(self, webdriver, df):
        for index, itemRow in df.iterrows():
            print(itemRow.URL)
            webdriver.get(itemRow.URL)
            screenshotPath = "screenshot_" + str(index) + ".jpg"
            webdriver.save_screenshot(screenshotPath)
            kit.sendwhats_image(self.phoneNum, screenshotPath, itemRow.URL, tab_close=True)
            os.remove(screenshotPath)

    # create a panda dataframe, "Title, sponsored, price"
    # It will automatically go to the next page(Either to the end of the list or to the 3rd page)
    def getAllResultForPage(self, url, webdriver):
        webdriver.get(url)
        soup = BeautifulSoup(webdriver.page_source, "html.parser")
        nextPageLinkCss = []
        nextPageLink = webdriver.find_element(By.CLASS_NAME, "s-pagination-next")
        table_all_result = pd.DataFrame(columns=["Title", "Sponsored", "Price", "URL"])
        page_counter = 0
        # check only the first 2 page or the end of the list
        while "s-pagination-disabled" not in nextPageLinkCss and page_counter < 3:
            searchResults = soup.findAll("div", {"data-component-type": "s-search-result"})
            df = self.getPandaResult(searchResults)
            table_all_result = pd.concat([table_all_result, df])
            # go to the next page every 2 second
            nextPageLink.click()
            nextPageLink = webdriver.find_element(By.CLASS_NAME, "s-pagination-next")
            nextPageLinkCss = nextPageLink.get_attribute("class").split()
            time.sleep(2)
            page_counter += 1
            if "s-pagination-disabled" in nextPageLinkCss:
                print("Reached the last page.")
        return table_all_result

    def run(self):
        # set up environment
        webdriver = self.wd.Chrome()
        webdriver.implicitly_wait(10)
        # open amazon website
        webdriver.get("http://amazon.com")
        # Enter zip code
        postcode_location = webdriver.find_elements(By.ID, "nav-global-location-popover-link")
        if postcode_location:
            postcode_location[0].click()
            postcode_area = webdriver.find_elements(By.ID, "GLUXZipUpdateInput")
            # If Zip code exists, then ignore it and press "Done" button
            # If zip code does not exist, then enter zip code
            # and press "Apply" button, then "Done" button
            if postcode_area:
                postcode_area[0].send_keys(self.zipcode)
                webdriver.find_element(By.ID, "GLUXZipUpdate").click()
            webdriver.find_element(By.NAME, "glowDoneButton").click()
        while True:
            df = self.getAllResultForPage(self.item_url, webdriver)
            df_query = df[df.Title.str.contains(str(self.keyword)) & (df.Price.astype(float) <= self.maxPrice)]
            if not df_query.empty:
                print("Found Items")
                print(df_query)
                self.sendWhatsAppMsg(webdriver, df_query)
                break
            else:
                time.sleep(60)
