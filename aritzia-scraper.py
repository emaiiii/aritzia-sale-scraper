import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

PATH = 'C:\\Users\\Erik\\Documents\\Projects\\python\\aritzia-scraper\\chromedriver.exe'
url = 'https://www.aritzia.com/us/en/sale?lastViewed=37'

driver = webdriver.Chrome(PATH)
driver.get(url)

last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(4)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 2);")

    # Wait to load page
    time.sleep(2)

html = driver.page_source

driver.quit()

#response = requests.get(url)
soup = BeautifulSoup(html, 'html.parser')

clothing_items = soup.findAll('div', {'class':'product-info'})

rows = []
columns = ['product_brand', 'product_name', 'product_price', 'product_sale_price']

for item in clothing_items:
    product_brand = str(item.findAll('div', {'class' : 'product-brand'})[0].a.text.strip())
    product_name = str(item.findAll('div', {'class' : 'product-name'})[0].a.text.strip())
    product_price = str(item.findAll('div', {'class' : 'product-pricing'})[0].select('span')[0].text.strip())
    product_sale_price = str(item.findAll('div', {'class' : 'product-pricing'})[0].select('span')[2].text.strip())

    print('brand: ' + product_brand + '\n')
    print('name: ' + product_name + '\n')
    print('price: ' + product_price + '\n')
    print('sale price: ' + product_sale_price + '\n')

    row = [product_brand, product_name, product_price, product_sale_price]
    rows.append(row)

df = pd.DataFrame(rows, columns=columns)
df.to_excel('aritzia_sale.xlsx', index=False)
print('file saved...')

 
