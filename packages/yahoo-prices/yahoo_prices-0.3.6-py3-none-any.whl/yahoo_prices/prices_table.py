"""
Defining the schema for prices table
"""

from sqlalchemy import create_engine, Column, DateTime, Integer, Float, String
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Prices(Base):

    """
    A class using Declarative at a minimum needs a __tablename__ attribute,
    and at least one Column which is part of a primary key 1.
    SQLAlchemy never makes any assumptions by itself about the table to which a class refers,
    including that it has no built-in conventions for names, datatypes, or constraints.
    """

    __tablename__ = "Prices"

    id = Column(Integer, primary_key=True)
    Ticker = Column(String(32))
    Date = Column(DateTime)
    High = Column(Float(3))
    Low = Column(Float(3))
    Open = Column(Float(3))
    Close = Column(Float(3))
    Volume = Column(Float(3))
    AdjClose = Column(Float(3))

    __table_args__ = (
                      UniqueConstraint('Ticker', 'Date', name='Ticker_Date'),
                     )

def create_table():
    """
    creates sqlalchemy db engine
    """
    engine = create_engine('sqlite:///./prices.db', echo=False)
    if not engine.dialect.has_table(engine, 'Prices'):
        Base.metadata.create_all(engine)
    return engine
