from sqlalchemy.sql import exists, select, text

def create_new_schema(schema_name, session, debug=False):
    q_check_schema = exists(
        select([text("schema_name")]).select_from(text("information_schema.schemata")).
        where(text(f"schema_name = '{schema_name}'"))
    )
    if not debug:
        if not session.query(q_check_schema).scalar():
            session.execute(f"CREATE SCHEMA {schema_name};")
            session.commit()
            return True
        else:
            return False
        
    else:
        return session.query(q_check_schema)
