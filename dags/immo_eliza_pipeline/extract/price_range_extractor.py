import requests
import csv
from typing import List, Tuple
import time

# If you crawl for more than 2050 results, the api starts to loop and send you back the first results
HARD_LIMIT = 2050
HEADER = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}


def get_number_of_matches(
    session: requests.Session,
    min_price: int = 0, 
    max_price: int = 50_000, 
    min_rating: int = 0, 
) -> int:
    search_result = requests.get(
        url="https://www.vivino.com/api/explore/explore",
        params= {
            "min_rating": min_rating,
            "price_range_max": max_price,
            "price_range_min": min_price,
            "per_page": 5,
            "page": 1,
        },
        headers=HEADER
    )
    if search_result.status_code != 200:
        raise Exception(f"Could not find matches: {search_result.status_code}")
    
    
    wine_matches_number = search_result.json().get("explore_vintage", {}).get("records_matched")
    print(f"Found {wine_matches_number} matching wines!")
    return wine_matches_number


def save_price_ranges(price_ranges: List[Tuple[float, float, int]]) -> None:
    print("Saving price ranges...")
    with open('price_ranges.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["min_price", "max_price", "number_of_matches"])
        for min_price, max_price, number_of_matches in price_ranges:
            writer.writerow([min_price, max_price, number_of_matches])
    print("price ranges saved!")


def get_price_ranges(min_price: int = 0, max_price: int = 10_000) -> List[Tuple[float, float, int]]:
    """Get prices ranges that only return price ranges containing less than HARD_LIMIT wines."""
    price_ranges = []
    session = requests.Session()
    # Handle big price ranges
    # I do that to avoid iterating a lot in those big ranges that are mostly empty
    big_range_threshold = 600
    if max_price > big_range_threshold:
        match_number = get_number_of_matches(session, big_range_threshold, max_price)
        print(f"Found {match_number} matches in big range: {min_price} {max_price}")
        price_ranges.append(tuple([big_range_threshold, max_price, match_number]))
        max_price = big_range_threshold
    
    while max_price > 0:
        match_number = get_number_of_matches(session, min_price, max_price)
        if match_number > HARD_LIMIT:
            reduced_min = (min_price + max_price) / 2
            min_price = round(reduced_min, 2)
            print('reduced price range to: ', min_price, max_price)
        else:
            print("price_range found: ", min_price, max_price)
            price_ranges.append((min_price, max_price, match_number))
            max_price, min_price = min_price, 0
        time.sleep(0.3)
    session.close()

    save_price_ranges(price_ranges)
    
    return price_ranges


def is_cached_price_ranges_valide() -> bool:
    price_range_to_update = []
    with open("price_ranges.csv", 'r') as file:
        price_ranges = csv.reader(file)
        # Skip the first csv line (headers)
        next(price_ranges)
        with requests.Session() as sess:
            for price_range in price_ranges:
                min_price, max_price, _ = price_range[0], price_range[1], price_range[2]
                new_number_of_matches = get_number_of_matches(sess, min_price, max_price)
                # If any price range exced the hardlimit, we need to re-compute all the price ranges
                if new_number_of_matches > HARD_LIMIT:
                    print(f"Hard limit exceded or price range: {min_price} - {max_price} with {new_number_of_matches} matches found!")
                    return False
    return True


def load_cached_price_ranges() -> List[List[float | int]]:
    
    with open("price_ranges.csv", 'r') as file:
        csv_reader = csv.reader(file)
        # Skip the first csv line (headers)
        next(csv_reader)
        price_ranges = [row for row in csv_reader]
        return price_ranges
    



if __name__ == "__main__":
    # price_ranges = get_price_ranges()
    # print(f"Found {len(price_ranges)} price ranges!")
    is_price_ranges_outdated = is_cached_price_ranges_valide()
    print(is_price_ranges_outdated)