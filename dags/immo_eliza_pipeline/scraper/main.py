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
    # Check env variable
    try:
        pipeline_id = os.environ["CUSTOM_PIPELINE_ID"]
        print("Pipeline ID: ", pipeline_id)
    except KeyError as missing_variable:
        raise ValueError(f"Missing environment variable: {missing_variable}")

    # Create a file name with the pipeline ID
    file_name = f"houses_{pipeline_id}.html"

    print("scrapping...")
    houses = scrape()
    print("scrapping Done")

    print("Saving file to local temp folder...")
    file_path = f"/tmp/{file_name}"
    with open(file_path, "w") as file:
        file.write(houses)
    print("Saving file to local Done")

    print("uploading...")
    upload_file(file_path, file_name)
    print("uploading Done")
