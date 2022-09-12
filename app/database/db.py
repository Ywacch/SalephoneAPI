import os
import databases
from sqlalchemy import create_engine
from app.database import tables
import socket


DATABASEURL = f"postgresql://{os.environ.get('salephone_user')}:{os.environ.get('salephone_pw')}@" \
              f"{os.environ.get('postgres_host_ip')}/{os.environ.get('salephone_dbname')}"

database = databases.Database(DATABASEURL)

engine = create_engine(DATABASEURL)

tables.metadata.create_all(engine)
