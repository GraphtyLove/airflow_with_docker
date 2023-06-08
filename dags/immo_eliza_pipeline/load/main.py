import json
from schema import (
    Country,
    Region,
    Grape,
    Winery,
    Wine,
    Vintage,
    Keyword,
    FlavorGroup,
    TopList,
)
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# Initiate a session
engine = create_engine("sqlite:///vivino.db")
Session = sessionmaker(bind=engine)


def populate_database(json_path: str = "data_cleaned.json") -> None:
    # Load json
    with open(json_path, "r") as file:
        wines = json.load(file)

    session = Session()
    # Loop over each entry
    for entry in wines:
        vintage_data = entry["vintage"]
        price_data = entry["price"]
        wine_data = vintage_data["wine"]
        region_data = wine_data["region"]
        country_data = region_data["country"]
        winery_data = wine_data["winery"]
        taste_data = wine_data["taste"]["structure"]
        flavors = wine_data["taste"]["flavor"]
        top_lists_data = vintage_data.get("top_list_rankings")

        # --- Create keywords ---
        for group in flavors:
            for keyword in group["primary_keywords"]:
                add_keyword = Keyword(id=keyword["id"], name=keyword["name"])
                session.add(add_keyword)
            for keyword in group["secondary_keywords"]:
                add_keyword = Keyword(id=keyword["id"], name=keyword["name"])
                session.add(add_keyword)
            # --- Create Groups ---
            add_flavor_group = FlavorGroup(group=group["group"])
            session.add(add_flavor_group)

        # --- Create Winery ---
        add_winery = Winery(id=wine_data["id"], name=wine_data["name"])
        session.add(add_winery)

        # --- Create Grape ---
        country_grapes = []
        for grape in country_data["must_used_grapes"]:
            add_grape = Grape(
                id=grape["id"], name=grape["name"], wines_count=grape["wines_count"]
            )
            country_grapes.append(add_grape)
            session.add(add_grape)

        # --- Create Country ---
        add_country = Country(
            code=country_data["code"],
            name=country_data["name"],
            regions_count=country_data["regions_count"],
            users_count=country_data["users_count"],
            wines_counts=country_data["wines_counts"],
            wineries_count=country_data["wineries_count"],
            most_used_grapes=country_grapes,
        )
        session.add(add_country)

        # --- Create Region---
        add_region = Region(
            id=region_data["id"],
            name=region_data["name"],
            country_code=region_data["country_code"],
        )
        session.add(add_region)

        # --- Create Wine ---
        add_wine = Wine(
            id=wine_data["id"],
            name=wine_data["name"],
            is_natural=wine_data["is_natural"],
            region_id=region_data["id"],
            winery_id=winery_data["id"],
            acidity=taste_data["acidity"],
            fizziness=taste_data["fizziness"],
            intensity=taste_data["intensity"],
            sweetness=taste_data["sweetness"],
            tannin=taste_data["tannin"],
            structure_user_count=taste_data["structure_user_count"],
        )
        session.add(add_wine)

        # --- Create Vintage ---
        add_vintage = Vintage(
            id=vintage_data["id"], name=vintage_data["name"], wine_id=wine_data["id"]
        )
        session.add(add_vintage)

        # --- Create Toplist---
        if top_lists_data:
            for top_list in top_list_data:
                add_top_list = TopList(
                    id=top_list["top_list"]["id"],
                    name=top_list["top_list"]["name"],
                    wines=wine_data["name"],
                )
                session.add(add_top_list)

    print("Adding wine to DB...")
    # Commit the session to write the changes to the database
    session.commit()
    print("done")


if __name__ == "__main__":
    populate_database()
