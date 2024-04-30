import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import sqlite3

print("Running file...")

url = "https://www.jackery.com/collections/all"
response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")

product_containers = soup.find_all("div", class_="product-content-main")

product_names = []
discounted_prices = []
regular_prices = []
dates = []

for container in product_containers:
    product_name_elem = container.find("div", class_="product-title")
    product_name = product_name_elem.text.strip() if product_name_elem else "Product Name Not Found"
    
    discounted_price_elem = container.find("span", class_="price--on-sale")
    discounted_price = discounted_price_elem.text.strip() if discounted_price_elem else None
    
    product_prices_elem = container.find("div", class_="product-prices")
    span_tags = product_prices_elem.find_all("span")
    
    if len(span_tags) == 2:
        regular_price = span_tags[1].text.strip()
    elif len(span_tags) == 1:
        regular_price = span_tags[0].text.strip()
    else:
        regular_price = None
    
    product_names.append(product_name)
    discounted_prices.append(discounted_price)
    regular_prices.append(regular_price)
    
    current_date = datetime.now().strftime("%Y-%m-%d")
    dates.append(current_date)

data = {
    'Product Name': product_names,
    'Discounted Price': discounted_prices,
    'Regular Price': regular_prices,
    'Date': dates
}

df = pd.DataFrame(data)

conn = sqlite3.connect('jackery_prices.db')

df.to_sql('product_prices', conn, if_exists='append', index=False)

conn.commit()
conn.close()

print("\nProcess complete.")