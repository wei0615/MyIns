from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

HOST = '39.108.160.235'
POST = '3306'
DATABASE = 'tudo'
USERNAME = 'root'
PASSWORD = 'qwe123'

DB_URL = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(
    USERNAME,PASSWORD,HOST,POST,DATABASE
)

engine = create_engine(DB_URL,echo=True,pool_recycle=60)
DBSession = sessionmaker(bind=engine)
Base = declarative_base(engine)
