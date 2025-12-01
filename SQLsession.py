from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import  Column, Integer, String
from sqlalchemy.orm import Session
import psycopg2 # Иногда требуется для postgres
# Бибилотеки SQL

from decouple import Config, RepositoryEnv
ENV_FILE = 'e.env'
config = Config(RepositoryEnv(ENV_FILE))
# Подключение конфиг-файла


engine = create_engine(config('DB_LINK')) # create_async_engine()
SessionLocal = sessionmaker(autoflush=False, bind=engine) # async_sessionmaker()

Base.metadata.create_all(bind=engine) # Создание таблиц, если их нет