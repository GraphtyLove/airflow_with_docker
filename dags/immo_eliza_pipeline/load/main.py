import json
from dags.immo_eliza_pipeline.load.schema import (
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
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker


# Initiate a session
engine = create_engine("sqlite:///vivino.db")
Session = sessionmaker(bind=engine)


def populate_database(json_path: str = "data_cleaned.json") -> None:
    print("Creating database...")
    meta = MetaData()
    meta.create_all(engine)
    print("Database created.")

    print("Populating database...")
    print("Loading json...")
    # Load json
    with open(json_path, "r") as file:
        wines = json.load(file)
    print("Json loaded.")

    session = Session()
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

        # --- Create keywords ---
        for i_group, group in enumerate(flavors):
            print(f"Entry {i_entry+1}/{len(wines)} | Processing flavor group {i_group+1}/{len(flavors)}...")
            if group.get("primary_keywords"):
                for keyword in group["primary_keywords"]:
                    add_keyword = Keyword(id=keyword["id"], name=keyword["name"])
                    session.add(add_keyword)
            if group.get("secondary_keywords"):
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
        if country_data.get("must_used_grapes"):
            for i_grape, grape in enumerate(country_data["must_used_grapes"]):
                print(f"Entry {i_entry+1}/{len(wines)} | Processing grape {i_grape+1}"
                      f"/{len(country_data['must_used_grapes'])}...")
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
            wines_count=country_data["wines_count"],
            wineries_count=country_data["wineries_count"],
            most_used_grapes=country_grapes,
        )
        session.add(add_country)

        # --- Create Region---
        add_region = Region(
            id=region_data["id"],
            name=region_data["name"],
            country_code=country_data["code"],
        )
        session.add(add_region)

        # --- Create Wine ---
        add_wine = Wine(
            id=wine_data["id"],
            name=wine_data["name"],
            is_natural=wine_data["is_natural"],
            region_id=region_data["id"],
            winery_id=winery_data["id"],
            acidity=taste_data["acidity"] if taste_data else None,
            fizziness=taste_data["fizziness"] if taste_data else None,
            intensity=taste_data["intensity"] if taste_data else None,
            sweetness=taste_data["sweetness"] if taste_data else None,
            tannin=taste_data["tannin"] if taste_data else None,
            user_structure_count=taste_data["user_structure_count"] if taste_data else None,
        )
        session.add(add_wine)

        # --- Create Vintage ---
        add_vintage = Vintage(
            id=vintage_data["id"], name=vintage_data["name"], wine_id=wine_data["id"]
        )
        session.add(add_vintage)

        # --- Create Toplist---
        if top_lists_data:
            for i_top_list, top_list in enumerate(top_lists_data):
                print(f"Entry {i_entry+1}/{len(wines)} | Processing top list {i_top_list+1}/{len(top_lists_data)}...")
                add_top_list = TopList(
                    id=top_list["top_list"]["id"],
                    name=top_list["top_list"]["name"],
                    # TODO: To be update to append instead of overwrite
                    wines=[add_wine],
                )
                session.add(add_top_list)

    print("Adding wine to DB...")
    # Commit the session to write the changes to the database
    session.commit()
    print("done")


if __name__ == "__main__":
    populate_database()
