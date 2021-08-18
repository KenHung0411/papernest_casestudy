import pandas as pd
from sqlalchemy import create_engine, engine
import psycopg2
import os

class dbService:
    sql_query = '''
        SELECT 
            id,
            "FirstName",
            "LastName",
            "PhoneNumber",
            "CreationDate"
        FROM clients_crm
    '''

    def __init__(self, username, password, host_name, db_name):
        self.username = username
        self.password = password
        self.host_name = host_name
        self.db_name = db_name
        self.connect_string =  f"postgresql+psycopg2://{username}:{password}@{host_name}/{db_name}"

    def connect_db(self):
        engine  = create_engine(self.connect_string)
        return engine.connect()



    def read_table_through_df(self):
        with self.connect_db() as conn:
            df = pd.read_sql(self.sql_query, conn)
        return df



if __name__ == "__main__":
    user_name = os.environ["USER_NAME"]
    password = os.environ["PASSWORD"]
    host_name = os.environ["HOST_NAME"]
    db_name = os.environ["DB_NAME"]

    db_service = dbService(user_name, password, host_name, db_name)
    df = db_service.read_table_through_df()
    print(df.head())


