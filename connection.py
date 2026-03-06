from sqlalchemy import create_engine
from dotenv import load_dotenv
import pandas as pd
from os import environ

load_dotenv()

def con_engine():
    engine = create_engine(environ['DATABASE_URL'])
    return engine

if __name__ == '__main__':
    engine = con_engine()
    df = pd.read_sql_query('select * from public.usuarios', con=engine)
    print(df)