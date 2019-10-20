import json
import os
from models.recipes import Recipe, RecipeCategories, RecipeDirections, RecipeIngredients, RecipeRecommendations, Base

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from utils import tyler_local_connect, create_new_schema

path_to_app_settings = os.path.abspath('appsettings.json')

engine = tyler_local_connect(path_to_app_settings)

Session = sessionmaker(bind=engine, autoflush=False)
session = Session()


def coalesce_objects(json_data, desired_key, replaced_key):
    replacement_dict = {
        desired_key : [entry.get(desired_key) for entry in json_data],
        replaced_key : [entry.get(replaced_key) for entry in json_data]
    }

    replacement_data = [x if x else y for x, y in zip(replacement_dict[desired_key],  replacement_dict[replaced_key])]
    
    for ind, entry in enumerate(json_data):
        entry[desired_key] = replacement_data[ind]
        try:
            del entry[replaced_key]
        except KeyError:
            continue
    
    print(set().union(*(d.keys() for d in json_data)))

    return json_data

def insert_into_database(json_data):
    for i, entry in enumerate(json_data, start=1):

        ingredient_check = entry.pop('Ingredients', None)
        if ingredient_check:
            ingredients = [
                RecipeIngredients(IngredientFullText=ingredient) 
                for ingredient in ingredient_check
            ]
        else:
            ingredients=[]

        dir_check = entry.pop('Directions', None)
        if dir_check:
            directions = [
                RecipeDirections(
                    StepNumber=step, 
                    Instructions=instruction
                ) for step, instruction in dir_check
            ]
        else:
            directions = []

        rec_check = entry.pop('Recommendations', None)
        if rec_check:
            recommendations = [
                RecipeRecommendations(
                    Name=name,
                    URL=url
                ) for name, url in rec_check
            ]
        else:
            recommendations = []

        category_check = entry.pop('Categories', None)
        if category_check:
            categories = [
                RecipeCategories(
                    CategoryName=name, 
                    CategoryURL=url
                ) for name, url in category_check
            ]
        else:
            categories = []

        recipe = Recipe(
            **entry,
            ingredients=ingredients,
            directions=directions,
            recommendations=recommendations,
            categories=categories
        )

        session.add(recipe)
        session.add_all(ingredients)
        session.add_all(directions)
        session.add_all(recommendations)
        session.add_all(categories)

        if i % 1000 == 0:
            session.flush()
        
    session.commit()

def main():
    with open('data/remapped_fn_recipes.json', 'r') as fh:
        data = json.loads(fh.read())

    data = coalesce_objects(
        json_data=data,
        desired_key='Carbohydrates',
        replaced_key='Carbohydrate'
        )

    data = coalesce_objects(
        json_data=data,
        desired_key='DietaryFiber',
        replaced_key='Fiber'
        )

    for entry in data:
        try:
            entry['Authors'] = entry['Authors'][0]
        except IndexError:
            entry['Authors'] = None
        except TypeError:
            entry['Authors'] = None
            
    create_new_schema(
        schema_name=Recipe.__table_args__['schema'],
        session=session
    )

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    insert_into_database(data)

if __name__ == '__main__':
    main()