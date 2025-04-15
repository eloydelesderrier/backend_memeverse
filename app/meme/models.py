from sqlalchemy import Column, Integer, String, create_engine, MetaData, Table
import os


MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_PORT = os.getenv("MYSQL_PORT", 3306)
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")

DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"  

engine = create_engine(DATABASE_URL, echo=True)
metadata = MetaData()

