from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import json
from selenium import webdriver
import os, sys

def getHelp():
    os.system('cls' if os.name=='nt' else 'clear')
    print("Program is used to scrape data from different amazon websites to get data of best sellers in different categories. Program is suitable for scheduler and cronjobs.")
    print("\x1b[31mInformation: All data is accessible without any authentication and data doesn't include any sensitive information. Hence it can be used and completely legal.\x1b[0m")
    print("--------------------------------------------")
    print("Usage:")
    print("\tpy index.py [options]")
    print("--------------------------------------------")
    print("Options:")
    print("\t--help, Returns usage examples and valid console flags for the program.")
    print("\t--info-country, Returns the available country codes can be used during the scrape operation.")
    print("\t--scrape [countryCode], Starts the scraping operation for the specific amazon website.")
    print("\t\t For successful scraping the country code is required, Database must be validated and the credentials file must be provided according to description in the README.md file.")
    print("--------------------------------------------")
    

def getInfo(url_bases):
    os.system('cls' if os.name=='nt' else 'clear')
    print("For the following country codes the data can be scraped:")
    print("--------------------------------------------")
    for key, value in url_bases.items():
        print(f"\t{key} : {value.get('country')} ")
    print("--------------------------------------------")

def getCredentials(credentialFile):
    try:
        with open(f"{credentialFile}/amazonPipeline.json", "r") as file:
            creds = json.load(file)
            file.close()
            return {
                "connectionUrl": creds["dbUrl"],
                "collectionName": creds["collectionName"],
                "dbName": creds["dbName"],
            }
    except:
        print("Could not find credential file or credentials.")
        return None

def getCountryWebsite(base_urls,countryCode):
    for key, value in base_urls.items():
        if key == countryCode:
            return value.get("url")
    return False

def findPrice(item):
    if(item.find("span", {"class": "a-color-price"})):
        price = item.find("span", {"class": "a-color-price"}).text
        return price
    
    if(item.find("span", {"class": "a-size-base"})):
        price = item.select('span[class*="sc-price"]')[0].text
        return price
    
    return None

def getLinksFromList(data):
    links = []
    for el in data:
        link = el.find("a")
        if link:
            links.append(link["href"])
    return links or False

def getLinksFromPage(driver): 
    findDivPartialClassName = driver.find_element("xpath" , " /html/body/div[1]/div[1]/div[2]/div/div/div/div[2]/div/div[2]/div/div/div[2]")
    findAtags = findDivPartialClassName.find_elements(By.TAG_NAME, "a")
    links = [x.get_attribute("href")  for x in findAtags if x.get_attribute("href") != None]
    if len(links) == 0:
        links = False
    return links

def getScrapedDataFromLinks(driver, DB, url_base, credentials, links):
    scrapedTopList = {}
    for link in links:
        cleanedItems = []

        driver.get(link)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "lxml")

        xpath_list = [
            "/html/body/div[1]/div[2]/div/div/div[2]/div/div/div[2]/div[1]/span",
            "/html/body/div[1]/div[1]/div[2]/div/div/div/div[2]/div/div[2]/div/div/div[2]/div[1]/span",
        ]

        title = None

        for xpath in xpath_list:
            try:
                title_element = driver.find_element("xpath", xpath)
                title = title_element.text
                break
            except:
                pass

        if title:
            print("title: " + title, " url:", link)
            items = soup.find_all("div", {"id": "gridItemRoot"})
            for item in items:
                spans = item.find_all("span")
                rank = spans[0].text
                description = spans[1].text
                price = findPrice(item)

                link = item.find("a", {"class": "a-link-normal"})
                link = url_base + link["href"]

                cleanedData = {
                    "rank": rank,
                    "product": description,
                    "price": price,
                    "link": link,
                }
                cleanedItems.append(cleanedData)
            scrapedTopList[title] = cleanedItems
            time.sleep(4)
        else:
            print(title)
            print("title is not found for link: ", link)

        print("Getting the data")
    DB.insertDoc(credentials["collectionName"], scrapedTopList)
    return True

def scrapeData(DB, credentials, url_base):
    os.system('cls' if os.name=='nt' else 'clear')
    url = f"{url_base}/Best-Sellers/zgbs"
    if url_base == "https://www.amazon.com.tr":
        url = f"{url_base}/gp/bestsellers"
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome()
    driver.get(url)
    driver.implicitly_wait(2)

    linksList = getLinksFromPage(driver)
    if not linksList:
        print("No links found")
        sys.exit()

    scrapedData = getScrapedDataFromLinks(driver, DB, url_base, credentials, linksList)
    if scrapedData:
        print("Data scraped successfully.")
    else:
        print("While scraping data an error occured please check the logs.")
    
    DB.disconnectDb()
    