import glob
import os
import pandas as pd

import sqlalchemy.sql as sql
from utils import create_new_schema, create_session, tyler_local_connect

path_to_app_settings = os.path.abspath('appsettings.json')

engine = tyler_local_connect(path_to_app_settings)
session = create_session(engine)

def schema_create_test(schema_name='etl'):
    query_results = create_new_schema(
            schema_name=schema_name,
            session=session,
            debug=True
        )
    print(query_results.scalar())

def test_session_location():
    # query = sql.select([sql.text('database_name()')])
    # return session.query(query).all()
    
    print(engine.table_names())
    print(engine.schema_names())
if __name__ == '__main__':
    schema_create_test()
    print(test_session_location())
    session.close()
    engine.dispose()