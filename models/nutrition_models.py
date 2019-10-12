from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text

Base = declarative_base()

class BrandedFood(Base):
    __tablename__ = 'branded_food'
    __table_args__ = {'schema': 'fda'}

    fdc_id = Column(Integer, primary_key=True)
    brand_owner = Column(String)
    gtin_upc = Column(String)
    ingredients = Column(Text)
    serving_size = Column(Integer)
    serving_size_unit = Column(String)
    household_serving_text = Column(String)
    food_category = Column(String)
    data_source = Column(String)

    def __repr__(self):
        return f"<BrandedFood(owner={self.brand_owner}, type={self.food_category}, upc={gtin_upc})"



    