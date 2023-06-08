import json


def load_original_data(json_path: str = "../../../data.json") -> dict:
    print("loading data...")
    with open(json_path) as f:
        wines = json.load(f)
    print(f"Data loaded! Found {len(wines)} wines.")
    return wines


def save_file(data: dict, json_path: str = "../../../data_cleaned.json") -> None:
    print(f"Saving data to: {json_path}")
    # Save cleaned file
    with open("../../../data_cleaned.json", "w") as f:
        json.dump(data, f)
    print("Data saved!")
    return


def remove_useless_fields(wines: dict) -> dict:
    """
    Function that removes all the fields we don't need.

    This is there to make the data we are working with a lot lighter.
    """
    print("Removing useless fields...")
    for wine in wines:
        wine.pop("prices", True)
        # vintage
        vintage_keys_to_remove = ["seo_name", "image", "grapes", "has_valid_ratings"]
        for key in vintage_keys_to_remove:
            wine["vintage"].pop(key, True)
        # Wine
        wine_keys_to_remove = [
            "seo_name",
            "type_id",
            "has_valid_ratings",
            "style",
            "vintage_type",
        ]
        for key in wine_keys_to_remove:
            wine["vintage"]["wine"].pop(key, True)
        # Region
        if wine["vintage"]["wine"].get("region"):
            region_keys_to_remove = [
                "seo_name",
                "name_en",
                "class",
                "background_image",
                "native_name",
                "seo_name",
                "currency",
            ]
            for key in region_keys_to_remove:
                wine["vintage"]["wine"]["region"].pop(key, True)
            # Country
            country_keys_to_remove = ["native_name", "seo_name", "currency"]
            for key in country_keys_to_remove:
                wine["vintage"]["wine"]["region"]["country"].pop(key, True)
            # Grapes
            for grape in wine["vintage"]["wine"]["region"]["country"][
                "most_used_grapes"
            ]:
                grape.pop("seo_name", True)
                grape.pop("has_detailed_info", True)
        # Winery
        winery_keys_to_remove = ["seo_name", "background_image", "status"]
        for key in winery_keys_to_remove:
            wine["vintage"]["wine"]["winery"].pop(key, True)

        wine["vintage"]["wine"]["url"] = wine.get("price", {}).get("url")
        # Price
        wine["price"]["bottle_volume_ml"] = (
            wine.get("price", {}).get("bottle_type", {}).get("volume_ml")
        )
        wine["price"]["amount_in_euros"] = wine.get("price", {}).get("amount")
        price_keys_to_remove = [
            "bottle_type",
            "amount",
            "currency",
            "id",
            "type",
            "sku",
            "url",
            "visibility",
            "bottle_type_id",
        ]
        for key in price_keys_to_remove:
            wine["price"].pop(key, True)
        # Top list ranking
        if wine["vintage"].get("top_list_rankings"):
            for rank in wine["vintage"]["top_list_rankings"]:
                rank.pop("description", True)
                rank["top_list"].pop("seo_name", True)
                rank["top_list"].pop("type", True)
                # Most of the time empty
                rank["top_list"].pop("year", True)
    print("Useless fields removed!")
    return wines


def remove_duplicates(wines: dict) -> dict:
    print("Removing duplicates...")
    unique_ids = []
    wine_without_duplicates = []

    for wine in wines:
        wine_id = wine["vintage"]["wine"]["id"]
        vintage_id = wine["vintage"]["id"]
        # Create a unique ID for each combo wine+vintage
        unique_id = f"{wine_id}-{vintage_id}"
        if unique_id not in unique_ids:
            unique_ids.append(unique_id)
            wine_without_duplicates.append(wine)

    duplicates_number = len(wines) - len(wine_without_duplicates)
    print(
        f"Duplicates removed! Found {duplicates_number} duplicates for {len(wine_without_duplicates)} non-duplicates"
    )
    return wine_without_duplicates


def preprocess():
    """Full preprocessing pipeline to clean scraped data."""
    print("Start preprocessing...")
    wines = load_original_data()
    wines = remove_useless_fields(wines)
    wines = remove_duplicates(wines)
    # Save final data
    save_file(wines, "../../../data_cleaned.json")
    # Save sample data
    save_file(wines[:2], "../../../data_cleaned_sample.json")


if __name__ == "__main__":
    preprocess()
