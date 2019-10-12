from bs4 import BeautifulSoup

from crawler_utils import RecipeWebsite, Recipe
from crawler_utils import download_sitemap_files
from collections import defaultdict
from pathlib import Path

import glob
import gzip
import json
import pprint
import requests
import sys
from unicodedata import normalize

sitemap_output_path = Path(__file__).parents[1].joinpath('data', 'sitemaps')

pp = pprint.PrettyPrinter(indent=4)

def read_sitemap(sitemap_path):
    sitemap_files = glob.glob(sitemap_path.joinpath('*.gz').as_posix())
    all_links = []
    for sitemap_file in sitemap_files:
        with gzip.open(sitemap_file) as fh:
            soup = BeautifulSoup(fh.read(), 'xml')\
        
        unique_recipes = set([link.loc.text for link in soup.find_all('url') if '/recipes/' in link.text])
        all_links.extend(unique_recipes)
        print(len(unique_recipes))
    
    all_links = set(all_links)
    print(len(all_links))

    with open(sitemap_output_path.joinpath('recipe_links_to_crawl.txt'), 'w') as fh:
        for link in all_links:
            fh.write(f'{link}\n')

    return list(all_links)


def extract_recipe_info(recipe_soup):
    recipe_dict = defaultdict(str)

    #Recipe Title
    recipe_title_section = recipe_soup.find('section', class_="o-AssetTitle")
    if recipe_title_section:
        recipe_dict['title'] = recipe_title_section.find('span', class_="o-AssetTitle__a-HeadlineText").text

    #TODO Must do Selenium crawl for ratings and reviews
    # recipe_rating = recipe_soup.find('span', class_="gig-rating-stars ").get('title')
    # recipe_review_count = recipe_soup.find('span', class_="gig-rating-ratingsum ").text

    # Recipe Authors
    recipe_author_section = recipe_soup.find('div', class_='o-Attribution__m-Author')
    if recipe_author_section:
        if not recipe_author_section.find('a'):
            recipe_dict['authors'] = [recipe_author_section.find('span', class_='o-Attribution__a-Name').text.strip().replace('Recipe courtesy of ', '')]
        else:
            recipe_dict['authors'] = list(set([a.text.strip().replace('Recipe courtesy of ', '') for a in recipe_author_section.find_all('a', class_='o-Attribution__a-Name')]))

    # Recipe Ingredients
    recipe_ingredient_section = recipe_soup.find('section', class_='o-Ingredients')
    if recipe_ingredient_section:
        recipe_dict['ingredients'] = list(set([normalize('NFKD', p.text) for p in recipe_ingredient_section.find_all('p', class_='o-Ingredients__a-Ingredient')]))

    # Recipe Directions
    recipe_directions_section = recipe_soup.find('section', class_='o-Method')
    if recipe_directions_section:
        recipe_dict['directions'] = list(enumerate([li.text.strip() for li in recipe_directions_section.find_all('li', class_='o-Method__m-Step')], 1))

    # Recipe Information
    recipe_info_section = recipe_soup.find('div', class_='o-RecipeInfo')
    if recipe_info_section:

        # Recipe Skill Level
        recipe_skill_level_entry = recipe_info_section.find('ul', class_='o-RecipeInfo__m-Level')
        if recipe_skill_level_entry:
            recipe_dict['skill_level'] = recipe_skill_level_entry.find('span', class_='o-RecipeInfo__a-Description').text

        # Recipe Times
        recipe_time_section = recipe_info_section.find('ul', class_='o-RecipeInfo__m-Time')
        if recipe_time_section:
            recipe_times = dict(list(zip(
                [item.text.lower().strip(':') + '_time' for item in recipe_time_section.find_all('span', class_='o-RecipeInfo__a-Headline')], 
                [item.text for item in recipe_time_section.find_all('span', class_='o-RecipeInfo__a-Description')]
            )))
            recipe_dict.update(recipe_times)

        # Recipe Yield
        recipe_yield_section = recipe_info_section.find('ul', class_='o-RecipeInfo__m-Yield')
        if recipe_yield_section:
            recipe_dict['recipe_yield'] = recipe_yield_section.find('span', class_='o-RecipeInfo__a-Description').text

    # Recipe Notes
    if recipe_soup.find('p', class_='o-ChefNotes__a-Description'):
        recipe_dict['notes'] = recipe_soup.find('p', class_='o-ChefNotes__a-Description').text.strip('*')

    # Recipe Nutrition
    recipe_nutrition_section = recipe_soup.find('section', class_='o-NutritionInfo')
    if recipe_nutrition_section:
        recipe_dict['nutrition_serving_size'] = recipe_nutrition_section.find('dd', class_='m-NutritionTable__a-Description--Primary').text
        recipe_nutrition = dict(list(zip(
                [item.text.lower().replace(' ', '_') for item in recipe_nutrition_section.find_all('dt', class_='m-NutritionTable__a-Headline')], 
                [item.text for item in recipe_nutrition_section.find_all('dd', class_='m-NutritionTable__a-Description')]
            )))
        recipe_dict.update(recipe_nutrition)

    # Recipe Categories
    recipe_category_section = recipe_soup.find('div', class_='o-Capsule__m-TagList m-TagList')
    if recipe_category_section:
        recipe_dict['categories'] = [(item.text, item.get('href').strip('//')) for item in recipe_category_section.find_all('a')]

    # Recipe Recommendations
    recipe_recommendations_section = recipe_soup.find('section', class_='o-Recommendations')
    if recipe_recommendations_section:
        recipe_dict['recommendations'] = list(zip(
                [item.get('title') for item in recipe_recommendations_section.find_all('a')], 
                [item.get('href').strip('//') for item in recipe_recommendations_section.find_all('a')]
            ))
    
    return recipe_dict


def crawl_food_network():
    food_network = RecipeWebsite('http://foodnetwork.com')
    
    for sitemap_directory_link in food_network.sitemaps:
        print(sitemap_directory_link)
        download_sitemap_files(
            sitemap_directory_link=sitemap_directory_link,
            local_download_path=sitemap_output_path
        )

    # with open(sitemap_output_path.joinpath('recipe_links_to_crawl.txt'), 'r') as fh:
    #     recipe_links = fh.readlines()

    recipe_links = read_sitemap(sitemap_output_path)
    crawled_recipes = []
    broken_links = []
    weird_json = []

    for recipe_link in recipe_links:
        try:
            recipe_html = requests.get(recipe_link)
        except:
            print(f'Could not establish connection to {recipe_link}.')
            continue
        recipe_soup = BeautifulSoup(recipe_html.text, 'html')

        try:
            recipe = Recipe(
                extract_recipe_info(recipe_soup), 
                website='Food Network',
                url=recipe_link.strip('\n')
                )
        except:
            broken_links.append(recipe_link)
        try:
            json.dumps(recipe.__dict__)
            crawled_recipes.append(recipe.__dict__)
        except:
            weird_json.append(recipe.__dict__)
        

    with open('broken_links.txt', 'w') as fh:
        for item in broken_links:
            fh.write(f'{item}\n')

    with open('weird_json.txt', 'w') as fh:
        for item in weird_json:
            fh.write(f'{item}\n\n')

    with open('food_network_recipes.json', 'w') as fh:
        json.dump(crawled_recipes, fh)

if __name__ == '__main__':
    try:
        crawl_food_network()
    except:
        print('Exiting early')
        with open('broken_links.txt', 'w') as fh:
            for item in broken_links:
                fh.write(f'{item}\n')

        with open('weird_json.txt', 'w') as fh:
            for item in weird_json:
                fh.write(f'{item}\n\n')

        with open('food_network_recipes.json', 'w') as fh:
            json.dump(crawled_recipes, fh)

    # recipe_link = 'https://www.foodnetwork.com/recipes/marcela-valladolid/jalapeno-buttered-corn-recipe-1920320'
    # recipe_html = requests.get(recipe_link)
    # recipe_soup = BeautifulSoup(recipe_html.text)
    
    # recipe_dict = extract_recipe_info(recipe_soup)
    # print(recipe_dict)

