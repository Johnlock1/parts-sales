import os
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(os.getenv("DATABASE_URL"))


def import_file(file):
    try:
        filename = file.filename
        # filename = r'2018-12-16.xlsx'
        print(filename)
        df = pd.read_excel(filename)
        df.to_sql('sales', engine, if_exists='append', index=False)
    except Exception as e:
        print(e)
