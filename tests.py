import glob
import os
import pandas as pd

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
    
if __name__ == '__main__':
    schema_create_test()
    session.close()
    engine.dispose()