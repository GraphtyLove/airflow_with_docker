import json
import time
from collections import defaultdict
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dags.immo_eliza_pipeline.load.schema import (
    Country,
    Region,
    Grape,
    Winery,
    Wine,
    Vintage,
    Keyword,
    TopList,
    WineKeywords,
    MostUsedGrapesPerCountry,
    VintageTopListsRankings
)

# Initiate a session
engine = create_engine("sqlite:///vivino.db")
Session = sessionmaker(bind=engine)


def execution_time_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time

        hours = int(execution_time // 3600)
        minutes = int((execution_time % 3600) // 60)
        seconds = int(execution_time % 60)

        print(f"Execution time: {hours}h {minutes}m {seconds}s")
        return result

    return wrapper


@execution_time_decorator
def populate_database(json_path: str = "data_cleaned.json") -> None:
    print("Populating database...")
    print("Loading json...")
    # Load json
    with open(json_path, "r") as file:
        wines = json.load(file)
    print("Json loaded.")

    session = Session()

    keywords = defaultdict(Keyword)
    wineries = defaultdict(Winery)
    grapes = defaultdict(Grape)
    countries = defaultdict(Country)
    regions = defaultdict(Region)
    wines_db = defaultdict(Wine)
    vintages = defaultdict(Vintage)
    top_lists = defaultdict(TopList)
    keywords_wine = defaultdict(WineKeywords)
    most_used_grapes_per_country = defaultdict(MostUsedGrapesPerCountry)
    vintage_top_lists_rankings = defaultdict(VintageTopListsRankings)

    # Loop over each entry
    for i_entry, entry in enumerate(wines):
        print(f"Processing entry {i_entry+1}/{len(wines)}...")
        vintage_data = entry["vintage"]
        price_data = entry["price"]
        wine_data = vintage_data["wine"]
        region_data = wine_data["region"]
        country_data = region_data["country"]
        winery_data = wine_data["winery"]
        taste_data = wine_data["taste"]["structure"]
        flavors = wine_data["taste"]["flavor"]
        top_lists_data = vintage_data.get("top_list_rankings")

        for i_group, group in enumerate(flavors):

            if group.get("primary_keywords"):
                for keyword in group["primary_keywords"]:
                    # Create keyword if not exists
                    keywords[keyword["id"]] = Keyword(
                        id=keyword["id"],
                        name=keyword["name"],
                    )
                    # Add keyword to keywords_wine
                    keywords_wine[f"{keyword['id']}-{wine_data['id']}-{group['group']}"] = WineKeywords(
                        keyword_id=keyword["id"],
                        wine_id=wine_data["id"],
                        group_name=group["group"],
                        keyword_type="primary",
                        count=keyword["count"],
                    )

            if group.get("secondary_keywords"):
                for keyword in group["secondary_keywords"]:
                    # Create keyword if not exists
                    keywords[keyword["id"]] = Keyword(
                        id=keyword["id"],
                        name=keyword["name"],
                    )
                    # Add keyword to keywords_wine
                    keywords_wine[f"{keyword['id']}-{wine_data['id']}-{group['group']}"] = WineKeywords(
                        keyword_id=keyword["id"],
                        wine_id=wine_data["id"],
                        group_name=group["group"],
                        keyword_type="secondary",
                        count=keyword["count"],
                    )
        # Create winery if not exists
        wineries[wine_data["id"]] = Winery(id=wine_data["id"], name=wine_data["name"])

        if country_data.get("most_used_grapes"):
            for i_grape, grape in enumerate(country_data["most_used_grapes"]):
                # Create grape if not exists
                grapes[grape["id"]] = Grape(
                    id=grape["id"], name=grape["name"]
                )
                # Add grape to most_used_grapes_per_country
                most_used_grapes_per_country[f"{grape['id']}-{country_data['code']}"] = MostUsedGrapesPerCountry(
                    grape_id=grape["id"],
                    country_code=country_data["code"],
                    wines_count=grape["wines_count"],
                )

        # Create country if not exists
        countries[country_data["code"]] = Country(
            code=country_data["code"],
            name=country_data["name"],
            regions_count=country_data["regions_count"],
            users_count=country_data["users_count"],
            wines_count=country_data["wines_count"],
            wineries_count=country_data["wineries_count"],
        )

        # Create region if not exists
        regions[region_data["id"]] = Region(
            id=region_data["id"],
            name=region_data["name"],
            country_code=country_data["code"],
        )

        # Create wine if not exists
        wines_db[wine_data["id"]] = Wine(
            id=wine_data["id"],
            name=wine_data["name"],
            is_natural=wine_data["is_natural"],
            region_id=region_data["id"],
            winery_id=winery_data["id"],
            ratings_average=wine_data["statistics"]["ratings_average"],
            ratings_count=wine_data["statistics"]["ratings_count"],
            url=wine_data["url"],
            acidity=taste_data["acidity"] if taste_data else None,
            fizziness=taste_data["fizziness"] if taste_data else None,
            intensity=taste_data["intensity"] if taste_data else None,
            sweetness=taste_data["sweetness"] if taste_data else None,
            tannin=taste_data["tannin"] if taste_data else None,
            user_structure_count=taste_data["user_structure_count"] if taste_data else None,
        )

        # Create vintage if not exists
        vintages[vintage_data["id"]] = Vintage(
            id=vintage_data["id"],
            name=vintage_data["name"],
            wine_id=wine_data["id"],
            ratings_average=vintage_data["statistics"]["ratings_average"],
            ratings_count=vintage_data["statistics"]["ratings_count"],
            year=vintage_data["year"],
            price_euros=price_data["amount_in_euros"] if price_data else None,
            price_discounted_from=price_data["discounted_from"] if price_data else None,
            price_discount_percentage=price_data["discount_percent"] if price_data else None,
            bottle_volume_ml=price_data.get("bottle_volume_ml"),
        )

        if top_lists_data:
            for top_list_ranking in top_lists_data:
                # Create top_list if not exists
                country_code = top_list_ranking["top_list"]["location"].split("_")[0]
                top_lists[top_list_ranking["top_list"]["id"]] = TopList(
                    id=top_list_ranking["top_list"]["id"],
                    name=top_list_ranking["top_list"]["name"],
                    country_code=country_code if country_code else "global",
                )
                # Add top_list to vintage_top_lists_rankings
                vintage_top_lists_rankings[f"{top_list_ranking['top_list']['id']}-{vintage_data['id']}"] = \
                    VintageTopListsRankings(
                    top_list_id=top_list_ranking["top_list"]['id'],
                    vintage_id=vintage_data["id"],
                    rank=top_list_ranking["rank"],
                    previous_rank=top_list_ranking["previous_rank"],
                )

    # Bulk insertion
    objects_to_insert = [
        keywords, wineries, grapes, countries, regions, wines_db, vintages, top_lists, keywords_wine,
        most_used_grapes_per_country, vintage_top_lists_rankings
    ]
    print("Bulk inserting data...")
    for i, objects in enumerate(objects_to_insert):
        print(f"Inserting {len(objects)} objects | Query: {i}/{len(objects_to_insert)}...")
        session.bulk_save_objects(objects.values())
    # Commit the session to write the changes to the database
    print("Objects inserted. Committing...")
    session.commit()
    print("Done.")


if __name__ == "__main__":
    saving_path = os.environ.get("DATA_SHARED_PATH", "")
    data_path = os.path.join(saving_path, "data_cleaned.json")
    
    # Average time to process/insert ~79k wines from json to sqlite: ~2min 50s WITHOUT keywords
    # Average time to process/insert ~79k wines from json to sqlite: ~4min 50s WITH keywords
    # Average time to process/insert ~79k wines from json to sqlite: 5min 10s WITH keywords and top lists
    populate_database(data_path)
