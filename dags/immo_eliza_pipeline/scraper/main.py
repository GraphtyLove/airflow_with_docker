from typing import List
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from common import upload_file
import os

def scrape() -> str:
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = Chrome(options=options)
    
    driver.get('https://www.google.com/search?q=becode&oq=becode+&aqs=chrome..69i57j69i60j69i61l3j69i60j69i65l2.1248j0j4&sourceid=chrome&ie=UTF-8')
    page_html = driver.page_source

    return page_html


if __name__ == '__main__':
    print("scrapping...")
    houses = scrape()
    print("scrapping Done")

    print("uploading...")
    pipeline_id  = os.getenv("PIPELINE_ID")
    if not pipeline_id:
        raise ValueError("Pipeline ID not found")
    print("Pipeline ID: ", pipeline_id)
    print("Debug print")
    
    upload_file(houses, f"houses_{pipeline_id}.html")
    print("uploading Done")
