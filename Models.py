from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import  Column, Integer, String
import psycopg2 # Иногда требуется для postgres
# Бибилотеки SQL

from decouple import Config, RepositoryEnv
ENV_FILE = 'e.env'
config = Config(RepositoryEnv(ENV_FILE))
# Подключение конфиг-файла

# Создаем модель бд

class Base(DeclarativeBase): pass
class Entity(Base):
   __tablename__ = config('TABLE_NAME')

   id = Column(Integer, primary_key=True, index=True)
   name = Column(String)
   description = Column(String)
   likes = Column(Integer)