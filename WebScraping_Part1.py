import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

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
                product_name = container.find("span", class_="a-size-medium").text.strip()
                product_price = container.find("span", class_="a-offscreen").text.strip()
                product_rating = container.find("span", class_="a-icon-alt").text.strip()
                product_reviews = container.find("span", {"class": "a-size-base"}).text.strip()
                products.append({"Product URL": product_url, "Product Name": product_name, "Product Price": product_price, "Rating": product_rating, "Number of Reviews": product_reviews})
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
df.to_csv(r"amazon_scrape.csv", index=False)
