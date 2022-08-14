from sqlalchemy import Table, MetaData
from sqlalchemy import Column, ForeignKeyConstraint, ForeignKey
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

metadata = MetaData()
Base = declarative_base(metadata=metadata)


class Smartphones(Base):
    __tablename__ = 'smartphones'
    _id = Column('phone_id', postgresql.VARCHAR(32), primary_key=True)
    brand = Column('brand', postgresql.VARCHAR)
    series = Column('series', postgresql.VARCHAR)
    model = Column('model', postgresql.VARCHAR)
    name = Column('phone_name', postgresql.VARCHAR)
    size = Column('storage_size', postgresql.VARCHAR)
    listings = relationship("phonelistings")


class Listings(Base):
    __tablename__ = 'listings'
    _id = Column('item_id', postgresql.VARCHAR(12), primary_key=True)
    title = Column('title', postgresql.VARCHAR)
    global_id = Column('global_id', postgresql.VARCHAR)
    product_id = Column('product_id', postgresql.VARCHAR)
    postal_code = Column('postal_code', postgresql.VARCHAR)
    location_ = Column('location_', postgresql.VARCHAR)
    country = Column('country', postgresql.VARCHAR)
    currency = Column('currency', postgresql.VARCHAR)
    price = Column('price', postgresql.NUMERIC)
    condition_ = Column('condition_', postgresql.VARCHAR)
    shipping_type = Column('shipping_type', postgresql.VARCHAR)
    shipping_currency = Column('shipping_currency', postgresql.VARCHAR)
    shipping_cost = Column('shipping_cost', postgresql.NUMERIC)
    top_rated = Column('top_rated', postgresql.BOOLEAN)
    start_date = Column('start_date', postgresql.DATE)
    end_date = Column('end_date', postgresql.DATE)
    date_added = Column('date_added', postgresql.DATE, primary_key=True)
    listing_type = Column('listing_type', postgresql.VARCHAR)
    canadian_price_base = Column('canadian_price_base', postgresql.NUMERIC)
    canadian_total = Column('canadian_total', postgresql.NUMERIC)
    listings = relationship("phonelistings")


class Phonelistings(Base):
    __tablename__ = 'phonelistings',
    phone_id = Column('phone_id', postgresql.VARCHAR(32), ForeignKey("smartphones.phone_id"), primary_key=True)
    item_id = Column('item_id', postgresql.VARCHAR(12), primary_key=True)
    date = Column('date_added', postgresql.DATE, primary_key=True)
    __table_args__ = (
        ForeignKeyConstraint(["item_id", "date_added"], ["listings.item_id", "listings.date_added"]),
    )
