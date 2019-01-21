from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

HOST = '192.168.253.128'
POST = '3306'
DATABASE = 'tudo'
USERNAME = 'admin'
PASSWORD = 'Root110qwe'

DB_URL = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(
    USERNAME,PASSWORD,HOST,POST,DATABASE
)

engine = create_engine(DB_URL)
DBSession = sessionmaker(bind=engine)
Base = declarative_base(engine)
