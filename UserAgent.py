import time
from random import randrange
import pandas as pd
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from bs4 import BeautifulSoup
from tqdm import tqdm
from time import sleep
from fake_useragent import UserAgent

ua = UserAgent()

df = pd.DataFrame(columns=['Состояние', 'Производитель', 'Модель', 'Встроенная память','Цвет','Оперативная память','IMEI', 'Цена'])
Продолжение приложения
df.to_csv('dataset.csv', index=False)

with open('urls2.txt') as f:
    urls = list(set(f.read().splitlines()))

options = Options()
options.page_load_strategy = 'eager'

for page_url in tqdm(urls):
    options.add_argument(f'user-agent={ua.random}')  # Use a random User-Agent
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(page_url)
        contents = driver.page_source
        soup = BeautifulSoup(contents, "html.parser")

        item_parameters = soup.find_all("li", {"class": 'params-paramsList__item-appQw'})
        item_parameters = {item_parameter.text.split(': ')[0]: item_parameter.text.split(': ')[1] if len(item_parameter.text.split(': ')) > 1 else None for item_parameter in item_parameters}

        # Extract the price (adjust the index based on the correct position)
        price = soup.find_all("span", {"itemprop": "price"})
        price = price[1].text if len(price) > 1 else None
        item_parameters.update({'Цена': price})

        # Check if the key 'Код_производителя' already exists before updating
        if 'Код_производителя' in item_parameters:
            # Handle the case where the code is repeated
            code_occurrences = soup.find_all("li", {"class": 'params-paramsList__item-appQw', "title": "Код производителя"})
            if len(code_occurrences) > 1:
                # Choose the correct index based on the structure of the page
                manufacturer_code = code_occurrences[1].text.split(': ')[1]
                item_parameters['Код_производителя'] = manufacturer_code

        # Create a temporary DataFrame with current data
        df_temp = pd.DataFrame([item_parameters])

        # Check for the presence of data before adding to the main DataFrame
        if any(value is not None for value in item_parameters.values()):
            df = pd.concat([df, df_temp], ignore_index=True)
        else:
            print(f"Data is missing on the page: {page_url}")

    except Exception as e:
        print(f"An error occurred: {e}")
        time.sleep(randrange(1, 20))


    finally:
        driver.quit()
        time.sleep(randrange(1, 20))  # Add a delay before the next request

# Save the DataFrame to a CSV file after the loop
df.to_csv('dataset.csv', index=False)
