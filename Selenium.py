from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from tqdm import tqdm
import time
from random import randrange

options = Options()
options.page_load_strategy = 'eager'
driver = webdriver.Chrome(options=options)
CITY = 'amurskaya_oblast_blagoveschensk'
ITEM_TYPE = 'telefony'
def get_current_url_by_page(page_num=1, city=CITY,item_type=ITEM_TYPE):
    return f'https://www.avito.ru/{city}/{item_type}/mobile-ASgBAgICAUSwwQ2I_Dc?cd=1&p={page_num}'

driver.get(get_current_url_by_page(page_num=1))
count_items = int(driver.find_element(by=By.CSS_SELECTOR, value='span[data-marker="page-title/count"]').text.replace(" ", ""))
print(count_items)
count_pages = round(count_items/50)
print(count_pages)

# print(items)

for page_num in tqdm (range(0,count_pages)):
    items = driver.find_elements(by=By.CSS_SELECTOR, value='div[data-marker="item"]')
    with open(f"{page_num}.html", 'w', encoding='utf-8') as f:
        f.write(driver.page_source)

    for item in items:
        # try:

        url_element = item.find_element(by=By.CSS_SELECTOR, value='a[itemprop = "url"]')
        url = url_element.get_attribute("href")
        #print(url)
        with open('urls.txt', 'a') as url_file:
            url_file.write(url + '\n')
        # except StaleElementReferenceException:
        #     pass
    driver.find_element(by=By.CSS_SELECTOR, value='a[aria-label="Следующая страница"]').click()
    time.sleep(randrange(1, 20))