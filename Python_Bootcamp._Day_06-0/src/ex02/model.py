from sqlalchemy import Boolean, Column, Float, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()

SQLALCHEMY_DATABASE_URL = 'postgresql+psycopg2://postgres:lymondgl@localhost/ship_lymondgl'


class SpaceShip(Base):
    __tablename__ = "spaceship"
    id = Column(Integer, primary_key=True, index=True, unique=True)
    alignment = Column(String)
    name = Column(String)
    class_ship = Column(String)
    length = Column(Float)
    crew_size = Column(Integer)
    armed = Column(Boolean)
    officers_first_name = Column(String)
    officers_last_name = Column(String)
    officers_rank = Column(String)
