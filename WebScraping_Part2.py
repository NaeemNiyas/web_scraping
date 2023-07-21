import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_product_details(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        try:
            description = soup.find("div", {"id": "productDescription"}).text.strip()
        except AttributeError:
            description = "Nil"
        try:
            asin = soup.find("th", string="ASIN").find_next("td").text.strip()
        except AttributeError:
            asin = "Nil"
        try:
            product_description = soup.find("h1", {"id": "title"}).text.strip()
        except AttributeError:
            product_description = "Nil"
        try:
            manufacturer = soup.find("a", {"id": "bylineInfo"}).text.strip()
        except AttributeError:
            manufacturer = "Nil"

        product_details = {
            "Product URL": url,
            "Description": description,
            "ASIN": asin,
            "Product Description": product_description,
            "Manufacturer": manufacturer
        }
        return product_details
    else:
        print(f"Failed to fetch the page: {url}")
        return None

def scrape_products(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        products = []

        # Find product containers on the page
        product_containers = soup.find_all("div", {"data-component-type": "s-search-result"})

        for container in product_containers:
            try:
                product_url = "https://www.amazon.in" + container.find("a", class_="a-link-normal").get("href")
                product_info = scrape_product_details(product_url)
                if product_info:
                    products.append(product_info)
            except AttributeError:
                continue

        return products

    else:
        print(f"Failed to fetch the page: {url}")
        return None

base_url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_"
total_pages = 20
all_products = []

for page in range(1, total_pages + 1):
    url = base_url + str(page)
    print(f"Fetching URL: {url}")
    products_on_page = scrape_products(url)
    if products_on_page:
        all_products.extend(products_on_page)
    # time.sleep(3)  # Add a delay of 3 seconds between each page request

df = pd.DataFrame(all_products)
df.to_csv(r"amazon_scrape_with_details.csv", index=False)
