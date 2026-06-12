# Библиотеки SQL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# import psycopg2 
# Иногда требуется для postgres


# Библиотека для работы с config
from decouple import Config, RepositoryEnv


# Подключение конфиг-файла
ENV_FILE = 'e.env'
config = Config(RepositoryEnv(ENV_FILE))


engine = create_engine(config('DB_LINK')) 
SessionLocal = sessionmaker(autoflush=False, bind=engine) 

# create_async_engine()
# async_sessionmaker()


