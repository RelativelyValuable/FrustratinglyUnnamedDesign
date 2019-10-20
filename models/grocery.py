from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Store(Base):
    __tablename__ = 'Store'
    __table_args__ = {'schema' : 'grocery'}
    
    StoreID = Column(Integer, primary_key=True, autoincrement=True)
    StoreNumber = Column(Integer)
    Address = Column(String)
    State = Column(String)
    City = Column(String)
    StoreURL = Column(String)

    directions = relationship('Deals', lazy='dynamic', back_populates='store')

class Deals(Base):
    __tablename__ = 'Store'
    __table_args__ = {'schema' : 'grocery'}

    DealID = Column(Integer, primary_key=True, autoincrement=True)
    StoreID = Column(Integer, ForeignKey('grocery.Store.StoreID'))
    Product = Column(String)
    ProductSubtitle = Column(String)
    Offer = Column(String)
    Quantity = Column(String)
    Details = Column(String)

    store = relationship('Store')
    