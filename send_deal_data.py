import json
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.grocery import Base, Store, Deals
from utils import tyler_local_connect, create_new_schema

path_to_app_settings = os.path.abspath('appsettings.json')

engine = tyler_local_connect(path_to_app_settings)

Session = sessionmaker(bind=engine, autoflush=False)
session = Session()

create_new_schema(
    schema_name=Store.__table_args__['schema'],
    session=session
)

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

def main():
    with open("ht_locations.json", "r") as fh:
        locations = json.loads(fh.read())
    
    with open("ht_deals.json", "r") as fh:
        deals = json.loads(fh.read())
        
    flattened_loc_data = [location.update({"state" : state, "city" : city}) for state in list(locations.keys()) for city in locations[state] for location in city["locations"]]

if __name__ == "__main__":
    main()