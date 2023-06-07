import json
import os

with open("../../../data.json") as f:
    wines = json.load(f)

print(f"Found {len(wine_search)} wines.")

print("Removing useless data...")
for i, wine in enumerate(wines):
    wine.pop('prices', True)
    # vintage
    wine['vintage'].pop('seo_name', True)
    wine['vintage'].pop('image', True)
    wine['vintage'].pop('grapes', True)
    wine['vintage'].pop('has_valid_ratings', True)
    # Wine
    wine['vintage']['wine'].pop('seo_name', True)
    wine['vintage']['wine'].pop('type_id', True)
    wine['vintage']['wine'].pop('has_valid_ratings', True)
    wine['vintage']['wine'].pop('style', True)
    wine['vintage']['wine'].pop('vintage_type', True)
    # Region
    wine['vintage']['wine']['region'].pop('seo_name', True)
    wine['vintage']['wine']['region'].pop('name_en', True)
    wine['vintage']['wine']['region'].pop('class', True)
    wine['vintage']['wine']['region'].pop('background_image', True)
    # country 
    wine['vintage']['wine']['region']['country'].pop('native_name', True)
    wine['vintage']['wine']['region']['country'].pop('seo_name', True)
    # Winery
    wine['vintage']['wine']['winery'].pop('seo_name', True)
    wine['vintage']['wine']['winery'].pop('background_image', True)
    wine['vintage']['wine']['winery'].pop('status', True)

print("done")

print("all done! Saving results...")
with open("../../../data_cleaned.json", "w") as f:
    json.dump(wines, f)
print("results saved!")