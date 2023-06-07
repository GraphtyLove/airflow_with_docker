CREATE TABLE vintage (
  id INTEGER PRIMARY KEY,
  seo_name TEXT,
  name TEXT
);

CREATE TABLE statistics (
  vintage_id INTEGER PRIMARY KEY,
  status TEXT,
  ratings_count INTEGER,
  ratings_average REAL,
  labels_count INTEGER,
  wine_ratings_count INTEGER,
  wine_ratings_average REAL,
  wine_status TEXT
);

CREATE TABLE image (
  vintage_id INTEGER PRIMARY KEY,
  location TEXT
);

CREATE TABLE variations (
  vintage_id INTEGER PRIMARY KEY,
  bottle_large TEXT,
  bottle_medium TEXT,
  bottle_medium_square TEXT,
  bottle_small TEXT,
  bottle_small_square TEXT,
  label TEXT,
  label_large TEXT,
  label_medium TEXT,
  label_medium_square TEXT,
  label_small_square TEXT,
  large TEXT,
  medium TEXT,
  medium_square TEXT,
  small_square TEXT
);

CREATE TABLE wine (
  id INTEGER PRIMARY KEY,
  name TEXT,
  seo_name TEXT,
  type_id INTEGER,
  vintage_type INTEGER,
  is_natural INTEGER
);

CREATE TABLE region (
  id INTEGER PRIMARY KEY,
  name TEXT,
  name_en TEXT,
  seo_name TEXT,
  country_code TEXT
);


CREATE TABLE currency (
  code TEXT PRIMARY KEY,
  name TEXT,
  prefix TEXT,
  suffix TEXT
);

CREATE TABLE grape (
  id INTEGER PRIMARY KEY,
  name TEXT,
  seo_name TEXT,
  has_detailed_info INTEGER,
  wines_count INTEGER
);

CREATE TABLE winery (
  id INTEGER PRIMARY KEY,
  name TEXT,
  seo_name TEXT,
  status INTEGER
);

CREATE TABLE taste_structure (
  vintage_id INTEGER PRIMARY KEY,
  acidity REAL,
  fizziness REAL,
  intensity REAL,
  sweetness REAL,
  tannin REAL,
  user_structure_count INTEGER,
  calculated_structure_count INTEGER
);

CREATE TABLE flavor_group (
  vintage_id INTEGER PRIMARY KEY,
  "group" TEXT,
  count INTEGER,
  score INTEGER
);

CREATE TABLE flavor_keyword (
  group_vintage_id INTEGER,
  keyword_id INTEGER,
  name TEXT,
  count INTEGER,
  PRIMARY KEY (group_vintage_id, keyword_id)
);

CREATE TABLE secondary_keyword (
  group_vintage_id INTEGER,
  keyword_id INTEGER,
  name TEXT,
  count INTEGER,
  PRIMARY KEY (group_vintage_id, keyword_id)
);

CREATE TABLE class_typecast_map (
  vintage_id INTEGER PRIMARY KEY,
  background_image TEXT,
  class TEXT
);

CREATE TABLE class_background_image (
  vintage_id INTEGER PRIMARY KEY,
  location TEXT
);




CREATE TABLE country (
    code TEXT PRIMARY KEY,
    name TEXT,
    native_name TEXT,
    seo_name TEXT,
    currency_code TEXT,
    currency_name TEXT,
    currency_prefix TEXT,
    regions_count INTEGER,
    users_count INTEGER,
    wines_count INTEGER,
    wineries_count INTEGER
);

CREATE TABLE taste_flavor (
    wine_id INTEGER,
    "group" TEXT,
    flavor_count INTEGER,
    flavor_score REAL,
    FOREIGN KEY (wine_id) REFERENCES wine (id)
);


CREATE TABLE taste_primary_keyword (
    flavor_group TEXT,
    keyword_id INTEGER,
    keyword_name TEXT,
    keyword_count INTEGER,
    PRIMARY KEY (flavor_group, keyword_id)
);

CREATE TABLE taste_secondary_keyword (
    flavor_group TEXT,
    keyword_id INTEGER,
    keyword_name TEXT,
    keyword_count INTEGER,
    PRIMARY KEY (flavor_group, keyword_id)
);

