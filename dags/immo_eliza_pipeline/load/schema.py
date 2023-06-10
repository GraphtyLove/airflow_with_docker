from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
    Boolean,
    ForeignKey,
    Table,
    MetaData,
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

# # ------ Define the Association Tables ------
# toplist_wine = Table(
#     "toplist_wine",
#     Base.metadata,
#     Column("toplist_id", Integer, ForeignKey("toplists.id"), primary_key=True),
#     Column("wine_id", Integer, ForeignKey("wines.id"), primary_key=True),
# )


# ------ Define Tables schemas ------
class Country(Base):
    __tablename__ = "countries"
    code = Column(String, primary_key=True)
    name = Column(String)
    regions_count = Column(Integer)
    users_count = Column(Integer)
    wines_count = Column(Integer)
    wineries_count = Column(Integer)


class Region(Base):
    __tablename__ = "regions"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    country_code = Column(String, ForeignKey("countries.code"))


class Grape(Base):
    __tablename__ = "grapes"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    wines_count = Column(Integer)


class MostUsedGrapesPerCountry(Base):
    __tablename__ = "most_used_grapes_per_country"
    id = Column(Integer, primary_key=True, autoincrement=True)
    country_code = Column(String, ForeignKey("countries.code"))
    grape_id = Column(Integer, ForeignKey("grapes.id"))


class Winery(Base):
    __tablename__ = "wineries"
    id = Column(Integer, primary_key=True)
    name = Column(String)


class Wine(Base):
    __tablename__ = "wines"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    is_natural = Column(Boolean)
    region_id = Column(Integer, ForeignKey("regions.id"))
    winery_id = Column(Integer, ForeignKey("wineries.id"))
    ratings_average = Column(Float)
    ratings_count = Column(Integer)
    url = Column(String)
    acidity = Column(Float)
    fizziness = Column(Float)
    intensity = Column(Float)
    sweetness = Column(Float)
    tannin = Column(Float)
    user_structure_count = Column(Integer)


class Vintage(Base):
    __tablename__ = "vintages"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    wine_id = Column(Integer, ForeignKey("wines.id"))
    ratings_average = Column(Float)
    ratings_count = Column(Integer)
    year = Column(Integer)
    price_euros = Column(Float)
    price_discounted_from = Column(Float)
    price_discount_percentage = Column(Float)
    bottle_volume_ml = Column(Integer)


class FlavorGroup(Base):
    __tablename__ = "flavor_groups"
    name = Column(String, primary_key=True)


class Keyword(Base):
    __tablename__ = "keywords"
    id = Column(Integer, primary_key=True)
    name = Column(String)


class WineKeywords(Base):
    __tablename__ = "keywords_wine"
    keyword_id = Column(Integer, ForeignKey("keywords.id"), primary_key=True)
    wine_id = Column(Integer, ForeignKey("wines.id"), primary_key=True)
    group_name = Column(String, primary_key=True)
    keyword_type = Column(String)
    count = Column(Integer)


class TopList(Base):
    __tablename__ = "toplists"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    country_code = Column(String, ForeignKey("countries.code"))


class VintageTopListsRankings(Base):
    __tablename__ = "vintage_toplists_rankings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    top_list_id = Column(Integer, ForeignKey("toplists.id"))
    vintage_id = Column(Integer, ForeignKey("vintages.id"))
    rank = Column(Integer)
    previous_rank = Column(Integer)


if __name__ == "__main__":
    print("Creating DB...")
    engine = create_engine("sqlite:///vivino.db", echo=True)
    Base.metadata.create_all(engine)
    print("DB created!")
