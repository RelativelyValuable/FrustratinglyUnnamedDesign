from bs4 import BeautifulSoup
from collections import defaultdict
import json
import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as ec
import time

with open("appsettings.json", "r") as fh:
    config = json.loads(fh.read())

chromedriver_path = config['Chromedriver']["local_path"]
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("start-maximized")
prefs = {"profile.default_content_setting_values.geolocation" :2}
chrome_options.add_experimental_option("prefs", prefs)


def extract_state_list():
    state_index_page = requests.get("http://locations.harristeeter.com")
    soup = BeautifulSoup(state_index_page.text, 'html')
    states_to_crawl = [(li.span.text.title(), li.a.get("href")) for li in soup.find(id="state_list").find_all('li')]
    return states_to_crawl

def extract_city_list(state_url):
    state_page = requests.get(state_url)
    soup = BeautifulSoup(state_page.text, 'html')
    cities_to_crawl = [(city.text.strip('\n').title(), city.a.get("href")) for city in soup.find(id="cities").find_all("div", class_="city_item")]
    return cities_to_crawl

def extract_location_addresses(city_url):
    city_page = requests.get(city_url)
    soup = BeautifulSoup(city_page.text, 'html')
    stores_to_crawl = [(store.get("href").split('/')[-2], store.text.strip().replace("#", ""), store.get("href")) for store in soup.find(id="locations").find_all("a")]
    return stores_to_crawl

def extract_store_deals(address, driver):
    wait = WebDriverWait(driver, 10)
    driver.get('https://www.harristeeter.com/store-locator')
    overlay_close = wait.until(ec.element_to_be_clickable((By.XPATH, "//button[@ng-click='closeThisDialog()']")))
    overlay_close.click()
    wait.until(ec.invisibility_of_element_located((By.XPATH, "//button[@ng-click='closeThisDialog()']")))
    loc_search = driver.find_element_by_xpath("//input[@data-input='store-locator-input-enter-zip']")
    loc_search.send_keys(address)
    submit_btn = wait.until(ec.element_to_be_clickable((By.XPATH, "//button[@data-btn='store-locator-btn-enter-zip']")))
    submit_btn.click()
    try:
        select_store_btn = wait.until(ec.element_to_be_clickable((By.XPATH, "//div[@class='find_location_result']/div[@id='anchor1']/div[@class='find_location_result_left']/div[@class='find_location_result_right']/a[@class='btn grey ng-scope']")))
    except TimeoutException:
        select_store_btn = wait.until(ec.element_to_be_clickable((By.XPATH, "//div[@class='find_location_result']/div[@id='anchor1']/div[@class='find_location_result_left']/div[@class='find_location_result_right']/a[@class='btn grey']")))
    select_store_btn.click()
    select = Select(wait.until(ec.presence_of_element_located((By.ID, "departments"))))
    deal_options = select.options
    deals = []
    for i, option in enumerate(deal_options):
        select.select_by_index(i)
        deal_cat_dict = {"deal_category" : option.text, "deals" : []}
        try:
            wait.until(ec.presence_of_element_located((By.XPATH, "//div[@id='div_specials']/ul[@class='list-inline clearfix ng-scope']/li[@class='ng-scope'][1]/div[@class='productbox clearfix']/div[@class='product_infoBox']")))
        except TimeoutException:
            continue
        soup = BeautifulSoup(driver.page_source, 'html')
        for deal in soup.find("div", {"id" : "div_specials"}).find_all("li"):
            deal_dict = {}
            if deal.find("div", class_="product_title ng-binding"):
                deal_dict["product"] = deal.find("div", class_="product_title ng-binding").text.strip('\n')
            elif deal.find("div", class_="product_title"):
                deal_dict["product"] = deal.find("div", class_="product_title").text.strip('\n')

            if deal.find("span", class_="product_name_inner ng-binding"):
                deal_dict["product_sub"] = deal.find("span", class_="product_name_inner ng-binding").text.strip('\n')
            elif deal.find("span", class_="product_name_inner"):
                deal_dict["product_sub"] = deal.find("span", class_="product_name_inner").text.strip('\n')

            if deal.find("div", class_="product_size ng-binding"):
                deal_dict['quantity'] = deal.find("div", class_="product_size ng-binding").text.strip("\n")
            elif deal.find("div", class_="product_size"):
                deal_dict['quantity'] = deal.find("div", class_="product_size").text.strip("\n")

            if deal.find("span", class_="link ng-binding"):
                deal_dict['details'] = deal.find("span", class_="link ng-binding").text.strip("\n")
            elif deal.find("span", class_="link"):
                deal_dict['details'] = deal.find("span", class_="link").text.strip("\n")

            if deal.find("div", class_="offer_tag ng-binding"):
                deal_dict["offer"] = deal.find("div", class_="offer_tag ng-binding").text.strip('\n')
            elif deal.find("div", class_="offer_tag"):
                deal_dict["offer"] = deal.find("div", class_="offer_tag").text.strip('\n')

            deal_cat_dict["deals"].append(deal_dict)
        deals.append(deal_cat_dict)

    return deals

def main():
    locations = defaultdict(tuple)
    states_to_crawl = extract_state_list()
    for state, url in states_to_crawl:
        locations[state] = [{'city' : city, 'url': url} for city, url in  extract_city_list(url)]
        for city in locations[state]:
            city["locations"] = [{"store_number" : store_number, "address" : address, "url" : url} for store_number, address, url in extract_location_addresses(city["url"])]            

    with open('data/ht_locations.json', 'w') as fh:
        json.dump(locations, fh)
    
    with open('data/ht_locations.json', 'r') as fh:
        locations = json.loads(fh.read())
    
    store_list = [location for state in list(locations.keys()) for city in locations[state] for location in city["locations"]]
    driver = webdriver.Chrome(chromedriver_path, chrome_options=chrome_options)

    for store in store_list:
        try:
            store["all_deals"] = extract_store_deals(store["address"], driver)
        except:
            continue
    
    driver.close()

    with open("data/ht_deals.json", "w") as fh:
        json.dump(store_list, fh)

if __name__ == '__main__':
    main()