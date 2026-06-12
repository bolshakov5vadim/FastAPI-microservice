# Библиотеки SQL
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import  Column, Integer, String
from SQLsession import engine


# Библиотека для работы с config
from decouple import Config, RepositoryEnv


# Подключение config
ENV_FILE = 'e.env'
config = Config(RepositoryEnv(ENV_FILE))


# Создаем Entity
class Base(DeclarativeBase): pass
class Entity(Base):
   __tablename__ = config('TABLE_NAME')

   id = Column(Integer, primary_key=True, index=True)
   name = Column(String)
   description = Column(String)
   likes = Column(Integer)
   

# Создание таблиц, если их нет
Base.metadata.create_all(bind=engine) 
