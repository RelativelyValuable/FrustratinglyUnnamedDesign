from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Recipe(Base):
    __tablename__ = 'Recipe'
    __table_args__ = {'schema : etl.recipe'}
    
    RecipeID = Column(Integer, primary_key=True, autoincrement=True)
    Title = Column(String, nullable=False)
    Authors = Column(String)
    PrepTime = Column(String)
    CookTime = Column(String)
    ActiveTime = Column(String)
    InactiveTime = Column(String)
    TotalTime = Column(String)
    Yield = Column(String)
    SkillLevel = Column(String)
    WebsiteName =Column(String)
    URL =Column(String)
    NutritionServingSize = Column(String)
    Cholesterol = Column(String)
    TotalFat = Column(String)
    Carbohydrates = Column(String)
    DietaryFiber = Column(String)
    Sugar = Column(String)
    Fiber = Column(String)
    Sodium = Column(String)
    Calories = Column(String)
    SaturatedFat = Column(String)
    Protein = Column(String)

    directions = relationship('RecipeDirections', backref='Recipe')
    ingredients = relationship('RecipeIngredients', backref='Recipe')
    recommendations = relationship('RecipeRecommendations', backref='Recipe')


class RecipeDirections(Base):
    __tablename__ = 'Directions'
    __table_args__ = {'schema : etl.recipe'}

    DirectionID = Column(Integer, primary_key=True, autoincrement=True)
    RecipeID = Column(Integer, ForeignKey('Recipe.RecipeID'))
    StepNumber = Column(Integer)
    Instructions = Column(String)

    
class RecipeIngredients(Base):
    __tablename__ = 'Ingredients'
    __table_args__ = {'schema : etl.recipe'}

    IngredientID = Column(Integer, primary_key=True, autoincrement=True)
    RecipeID = Column(Integer, ForeignKey('Recipe.RecipeID'))
    IngredientFullText = Column(String)


class RecipeRecommendations(Base):
    __tablename__ = 'Recommendations'
    __table_args__ = {'schema' : 'etl.recipe'}

    RecommendationID = Column(Integer, primary_key=True, autoincrement=True)
    RecipeID = Column(Integer, ForeignKey('Recipe.RecipeID'))
    Name = Column(String)
    URL = Column(String)
    