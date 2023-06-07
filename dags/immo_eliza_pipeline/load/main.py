import sqlite3
import json

# Load data from JSON file
with open('data.json') as file:
    data = json.load(file)

# Connect to SQLite database
conn = sqlite3.connect('wine_data.db')
cursor = conn.cursor()

# Create tables
with open('create_tables.sql') as file:
    create_table_statements = file.read()

cursor.executescript(create_table_statements)
conn.commit()

# Insert data into tables
for entry in data:
    # Insert data into 'wine' table
    wine_values = (
        entry.get('id'),
        entry.get('name'),
        entry.get('type'),
        entry.get('region'),
        entry.get('country'),
        entry.get('description')
    )
    insert_wine = "INSERT INTO wine VALUES (?, ?, ?, ?, ?, ?);"
    cursor.execute(insert_wine, wine_values)

    # Insert data into 'rating' table
    rating_values = (
        entry.get('id'),
        entry.get('rating', {}).get('average_score'),
        entry.get('rating', {}).get('num_reviews')
    )
    insert_rating = "INSERT INTO rating VALUES (?, ?, ?);"
    cursor.execute(insert_rating, rating_values)

    # Insert data into 'taste_flavor' table
    for flavor in entry.get('taste_flavor', []):
        flavor_values = (
            entry.get('id'),
            flavor.get('group'),
            flavor.get('flavor_count'),
            flavor.get('flavor_score')
        )
        insert_taste_flavor = "INSERT INTO taste_flavor VALUES (?, ?, ?, ?);"
        cursor.execute(insert_taste_flavor, flavor_values)

# Commit the changes and close the connection
conn.commit()
conn.close()
