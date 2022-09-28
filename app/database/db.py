import os
import databases
from sqlalchemy import create_engine
from app.database import tables


DATABASEURL = f"postgresql://{os.environ.get('POSTGRES_USER')}:{os.environ.get('POSTGRES_PASSWORD')}@" \
              f"{os.environ.get('db_host')}/{os.environ.get('salephone_dbname')}"

database = databases.Database(DATABASEURL)

engine = create_engine(DATABASEURL)

tables.metadata.create_all(engine)
