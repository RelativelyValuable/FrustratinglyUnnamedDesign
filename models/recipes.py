from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Recipe(Base):
    __tablename__ = 'Recipe'
    __table_args__ = {'schema' : 'recipe'}
    
    RecipeID = Column(Integer, primary_key=True, autoincrement=True)
    Title = Column(String)
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
    Notes = Column(Text)

    directions = relationship('RecipeDirections', lazy='dynamic', back_populates='recipe')
    ingredients = relationship('RecipeIngredients', lazy='dynamic', back_populates='recipe')
    recommendations = relationship('RecipeRecommendations', lazy='dynamic', back_populates='recipe')
    categories = relationship('RecipeCategories', lazy='dynamic', back_populates='recipe')

class RecipeDirections(Base):
    __tablename__ = 'Directions'
    __table_args__ = {'schema' : 'recipe'}

    DirectionID = Column(Integer, primary_key=True, autoincrement=True)
    RecipeID = Column(Integer, ForeignKey('recipe.Recipe.RecipeID'))
    StepNumber = Column(Integer)
    Instructions = Column(String)

    recipe = relationship('Recipe')
    
class RecipeIngredients(Base):
    __tablename__ = 'Ingredients'
    __table_args__ = {'schema' : 'recipe'}

    IngredientID = Column(Integer, primary_key=True, autoincrement=True)
    RecipeID = Column(Integer, ForeignKey('recipe.Recipe.RecipeID'))
    IngredientFullText = Column(String)

    recipe = relationship('Recipe')

class RecipeRecommendations(Base):
    __tablename__ = 'Recommendations'
    __table_args__ = {'schema' : 'recipe'}

    RecommendationID = Column(Integer, primary_key=True, autoincrement=True)
    RecipeID = Column(Integer, ForeignKey('recipe.Recipe.RecipeID'))
    Name = Column(String)
    URL = Column(String)

    recipe = relationship('Recipe')
    
class RecipeCategories(Base):
    __tablename__ = 'Categories'
    __table_args__ = {'schema' : 'recipe'}

    CategoryID = Column(Integer, primary_key=True, autoincrement=True)
    RecipeID = Column(Integer, ForeignKey('recipe.Recipe.RecipeID'))
    CategoryName = Column(String)
    CategoryURL = Column(String)
    
    recipe = relationship('Recipe')
