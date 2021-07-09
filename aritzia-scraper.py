import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.aritzia.com/us/en/sale?lastViewed=37'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

clothing_items = soup.findAll('div', {'class':'product-info'})

rows = []
columns = ['product_brand', 'product_name', 'product_price', 'product_sale_price']


for item in clothing_items:
    product_brand = item.findAll('div', {'class' : 'product-brand'})[0].a.text
    product_name = item.findAll('div', {'class' : 'product-name'})[0].a.text
    product_price = item.findAll('div', {'class' : 'product-pricing'})[0].div.select('span')[0].text.strip()        
    product_sale_price = item.findAll('div', {'class' : 'product-pricing'})[0].div.select('span')[2].text.replace('\n', '').replace('-', ' - ')

    print('brand: ' + product_brand + '\n')
    print('name: ' + product_name + '\n')
    print('price: ' + product_price + '\n')
    print('sale price: ' + product_sale_price + '\n')

    row = [product_brand, product_name, product_price, product_sale_price]
    rows.append(row)


df = pd.DataFrame(rows, columns=columns)
df.to_excel('aritzia_sale.xlsx', index=False)
print('file saved...')

 
