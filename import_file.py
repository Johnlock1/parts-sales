import os
import pandas as pd
from sqlalchemy import create_engine
from app import UPLOAD_FOLDER

engine = create_engine(os.getenv("DATABASE_URL"))


def import_file(file):
    try:
        filename = file.filename
        path = UPLOAD_FOLDER + '/' + file.filename
        print(path)
        df = pd.read_excel(path)
        df.to_sql('sales', engine, if_exists='append', index=False)
    except Exception as e:
        print(e)
