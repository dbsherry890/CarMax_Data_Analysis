import furl
import math
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

baseUrl = "https://www.carmax.com/cars/api/search/run"

params = {"uri": "/cars/all", "skip": 0, "take": 1000, "radius": 90, "zipCode": 78747,
          "shipping": 20, "scoringProfile": "BestMatchScoreVariant3"}

# https://www.carmax.com/cars/api/search/run?uri=%2Fcars%2Fall&skip=96&take=24&zipCode=30334&radius=90&shipping=&sort=100&scoringProfile=BestMatchScoreVariant3

allItemsForSale = []
data = {}
csv_list = []


def constructUrl():
    global baseUrl
    global params

    f = furl.furl(baseUrl)
    f.args = params
    return f.url


def extractJsonFromSeleniumSource():
    global driver
    global data

    try:
        pre = driver.find_element(by=By.TAG_NAME, value="pre").text
        data = json.loads(pre)
    except Exception as e:
        print("exception occured", e)

    return data


def addEntriesToList(data):
    itemSaleList = data["items"]
    for i in range(len(itemSaleList)):
        allItemsForSale.append(itemSaleList[i])


if __name__ == '__main__':

    original_skip_value = params["skip"]

    driver = webdriver.Chrome()

    driver.get(constructUrl())

    # Display total CarMax listings for region selected
    totalListingsToGet = extractJsonFromSeleniumSource()["totalCount"]
    print("Listings to scrape: " + str(totalListingsToGet))

    for i in range(math.floor(totalListingsToGet / 100)):
        driver.get(constructUrl())

        addEntriesToList(extractJsonFromSeleniumSource())

        time.sleep(0.5)

        params["skip"] += 1000

    params["take"] = (totalListingsToGet % 1000)

    driver.get(constructUrl())
    addEntriesToList(extractJsonFromSeleniumSource())

    df = pd.DataFrame(allItemsForSale)
    df.to_csv('vehicle_features.csv')

    params["skip"] = original_skip_value
