import glob
import os
import pandas as pd

from utils import create_new_schema, create_session, tyler_local_connect

path_to_app_settings = os.path.abspath('appsettings.json')

engine = tyler_local_connect(path_to_app_settings)

def send_data_to_postgres(data_file, schema_name):
    df = pd.read_csv(data_file, low_memory=False)
    table_name = os.path.basename(data_file).strip(".csv")
    df.to_sql(
        name=table_name,
        con=engine,
        if_exists='replace',
        index=False,
        schema='etl'
    )

def main():
    schema_name = 'etl'
    schema_create_session = create_session(engine)

    create_new_schema(
        schema_name=schema_name,
        session=schema_create_session
    )


    for data_file in glob.glob("./data/FDAData/*.csv"):
        print(os.path.basename(data_file))
        send_data_to_postgres(
            data_file=data_file,
            schema_name=schema_name
        )


if __name__ == '__main__':
    main()
