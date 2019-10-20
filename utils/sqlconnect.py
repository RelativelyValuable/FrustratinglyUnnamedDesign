import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def _extract_postgres_settings(appsettings_file_path):
    with open('appsettings.json', 'r') as fh:
        settings = json.load(fh)

    postgres_configs = [config.items() for config in settings['Postgres']][0]
    postgres_connection_settings = {k : v for k, v in postgres_configs}

    return postgres_connection_settings

def tyler_local_connect(appsettings_file_path):
    postgres_connection_settings = _extract_postgres_settings(appsettings_file_path)
    ps = postgres_connection_settings['Tyler']
    engine = create_engine(
        "postgresql+psycopg2://" + ps["user"] + ":" + ps["password"] + "@" + ps["server"] + "/" + ps["database"],
        echo=False
    )

    return engine

def create_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()