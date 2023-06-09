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

# ------ Define the Association Tables ------
toplist_wine = Table(
    "toplist_wine",
    Base.metadata,
    Column("toplist_id", Integer, ForeignKey("toplists.id"), primary_key=True),
    Column("wine_id", Integer, ForeignKey("wines.id"), primary_key=True),
)


# ------ Define Tables schemas ------
class Country(Base):
    __tablename__ = "countries"
    code = Column(String, primary_key=True)
    name = Column(String)
    regions_count = Column(Integer)
    users_count = Column(Integer)
    wines_count = Column(Integer)
    wineries_count = Column(Integer)
    most_used_grapes = relationship("Grape")


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
    country_code = Column(String, ForeignKey("countries.code"))


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
    toplists = relationship("TopList", secondary=toplist_wine, back_populates="wines")
    flavor_groups = relationship("FlavorGroup", backref="wine")


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


class Keyword(Base):
    __tablename__ = "keywords"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    count = Column(Integer)
    keyword_type = Column(String) # primary or secondary
    flavor_group_id = Column(Integer, ForeignKey('flavor_groups.id'))

    # relationship to FlavorGroup
    flavor_group = relationship("FlavorGroup", back_populates="keywords")


class FlavorGroup(Base):
    __tablename__ = "flavor_groups"
    id = Column(Integer, primary_key=True, autoincrement=True)
    group_name = Column(String)
    wine_id = Column(Integer, ForeignKey('wines.id'))
    # Relationships
    wines = relationship("Wine", back_populates="flavor_groups")
    keywords = relationship("Keyword", back_populates="flavor_group")
    # primary_keywords = relationship("Keyword", secondary=flavor_group_keywords, backref="primary_flavor_groups")
    # secondary_keywords = relationship("Keyword", secondary=flavor_group_keywords, backref="secondary_flavor_groups")


class TopList(Base):
    __tablename__ = "toplists"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    wines = relationship("Wine", secondary="toplist_wine", back_populates="toplists")


if __name__ == "__main__":
    print("Creating DB...")
    engine = create_engine("sqlite:///vivino.db", echo=True)
    Base.metadata.create_all(engine)
    print("DB created!")
