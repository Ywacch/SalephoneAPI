from sqlalchemy import Table, MetaData
from sqlalchemy import Column
from sqlalchemy.dialects import postgresql

metadata = MetaData()

smartphones = Table(
    'smartphones',
    metadata,
    Column('phone_id', postgresql.VARCHAR(32), primary_key=True),
    Column('brand', postgresql.VARCHAR),
    Column('series', postgresql.VARCHAR),
    Column('model', postgresql.VARCHAR),
    Column('phone_name', postgresql.VARCHAR),
    Column('storage_size', postgresql.VARCHAR),
)
