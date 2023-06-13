import requests
import json
import time
import os
from price_range_extractor import get_price_ranges, is_cached_price_ranges_valide, load_cached_price_ranges


WINE_PER_PAGE = 50
HEADER = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}
saving_path = os.environ.get("DATA_SHARED_PATH", "")

def get_wines_from_page(
    page_number: int = 1,
    session: requests.Session | None = None, 
    min_rating: int = 0, 
    min_price: int = 0, 
    max_price: int = 10_000,
    language: str = "en"
) -> dict | None:
    """Function that scrap a single wine search page."""

    if session is None:
        session = requests.Session()

    search_result = session.get(
        url="https://www.vivino.com/api/explore/explore",
        params= {
            "min_rating": min_rating,
            "price_range_max": max_price,
            "price_range_min": min_price,
            "per_page": WINE_PER_PAGE,
            "page": page_number,
            "language": language,
        },
        headers=HEADER
    )
    if search_result.status_code != 200:
        print(f"Page {page_number} FAILED: {search_result.status_code}")
        return
    return search_result.json().get("explore_vintage", {}).get("matches")




if __name__ == "__main__":
    min_rating = 0
    min_price = 0
    max_price = 1_000_000
    language = "en"
    wines = []

    # If the first condition is met, won't check for the second
    if not os.path.isfile(os.path.join(saving_path, 'price_ranges.csv') or not is_cached_price_ranges_valide():
        price_ranges = get_price_ranges()
    else:
        price_ranges = load_cached_price_ranges()

    with requests.Session() as sess:
        price_range_index = 0
        for i, (min_price, max_price, number_of_matches) in enumerate(price_ranges):
            total_pages = int(number_of_matches) // WINE_PER_PAGE
            print(f"start scraping {total_pages} wines pages of price range {price_range_index + 1}/{len(price_ranges)}")
            try:
                for i in range(1, total_pages+1):
                    print(f"processing: {i}/{total_pages+1} of price range {price_range_index + 1}/{len(price_ranges)}")
                    wine = get_wines_from_page(i, sess, min_rating, float(min_price), float(max_price), language)
                    wines.extend(wine)
                    time.sleep(0.3)
                    
            except Exception as ex:
                print("Fatal error while scraping: ", ex)
            price_range_index += 1

    print("all done! Saving results...")
    
    with open(os.path.join(saving_path, "data.json"), "w") as f:
        json.dump(wines, f)
    print("results saved!")