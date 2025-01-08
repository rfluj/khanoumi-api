import requests
from bs4 import BeautifulSoup
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from database.db import connect_to_database, create_table, save_to_database, log_error

# URL to scrape
URL         = "https://www.khanoumi.com/api/ntl/v1/products?cat_id=27&page_size=24"
PRODUCT_URL = "https://www.khanoumi.com/products/"
PAGE_NUMBER = 1

def scrape_products(connection, url):
    """
    Scrape product details from the webpage.
    
    Returns:
        List[Dict]: A list of dictionaries containing product details.
    """
    response = requests.get(url)
    if response.status_code == 200:
        try:
            # Parse the JSON response
            data = response.json()
            products = data.get("data", {}).get("products", {}).get("items", [])
            if len(products) == 0:
                print("process is done!")
                return False
            
            # Extract relevant details
            for product in products:
                save_to_database(connection, {
                    "productUrl": generate_product_url(product.get("slug")),
                    "nameFa": product.get("nameFa"),
                    "nameEn": product.get("nameEn"),
                    "discountPrice": product.get("discountPrice"),
                    "basePrice": product.get("basePrice"),
                    "name": product.get("brand").get("nameEn"),
                    "imageUrl": product.get("imageUrl"),
                })
            return True
        
        except ValueError as e:
            print(f"Error parsing JSON: {e}")
            log_error(connection, url, response.status_code, error_message=e)
            return "json parser error."
    else:
        print(f"Failed to fetch the page {URL}. Status code: {response.status_code}")
        log_error(connection, url, response.status_code)
        return "network error."

def generate_product_url(slug):
    url = PRODUCT_URL + slug
    return url

def create_url():
    global PAGE_NUMBER  
    url         = URL + "&page_number=" + str(PAGE_NUMBER)
    PAGE_NUMBER += 1
    return url
    

def main():
    """
    Main function to scrape data and save to the database.
    """
    # Connect to the database
    connection = connect_to_database()
    if not connection:
        print("Database connection failed.")
        return

    # Create the table if it doesn't exist
    create_table(connection)

    # Scrape product details
    while True:
        url = create_url()
        res = scrape_products(connection, url)
        if not res:
            break

    # Close the database connection
    connection.close()

if __name__ == "__main__":
    main()
