from fastapi import FastAPI, Body, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import logging


# Объект для работы с БД
from sqlalchemy.orm import Session


# Библиотека стандартизации ответа
from pydantic import BaseModel


# Импорт из файлов
from SQLsession import SessionLocal
from Models import Entity


# Создание объекта логирования
logging.basicConfig(
    level = logging.INFO,
    format = "%(asctime)s-%(name)s-%(levelname)s-%(message)s",
    datefmt = "%Y-%m-%d %H:%M:%S",
    filename = "mylog.log"
)
logger = logging.getLogger(__name__)


# Создание объекта Response
class Response(BaseModel):
    id: int
    name: str
    description: str
    likes: int

    class ConfigDict:
        from_attributes = True 


# Функция, выдающая подключения к БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database session error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database connection error"
        )
    finally:
        db.close()
   

# API
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins = ['http://nginx_app'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    )


# Описание бизнес-логики
@app.get("/api", response_model = Response)
def read(data  = Body(), db: Session = Depends(get_db)):
    """Маршрут предоставляет сущности в постраничном виде. Номер страницы берется из поля ["page"] запроса."""
    try:

        if(data["page"]): entity = db.query(Entity).limit(10).offset((data["page"] - 1) * 10).all()
        return Response.from_orm(entity)

    except Exception as e:
        logger.error("Error requesting for page "+data["page"])
        raise HTTPException(status_code=404, detail="Пользователь не найден")


  
@app.post("/api", response_model = Response)
def create(data  = Body(), db: Session = Depends(get_db)):
    """Маршрут сохраняет отправленную сущность в БД. Сущность берётся из полей ["name"] ["description"] ["likes"]."""
    try:

        entity = Entity(name=data["name"], description=data["description"], likes=data["likes"])
        # Если используется auto-increment, не нужно отправлять id 

        db.add(entity) # await
        db.commit()
        db.refresh(entity)
        logger.info(f"Data posted")
        return Response.from_orm(entity)
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating entity: "+str(e))
        raise HTTPException(status_code=404, detail="Пользователь не создан")

  
@app.delete("/api/{id}")
def delete(id: int, db: Session = Depends(get_db)):
    """Маршрут удаляет сущность по её ID. ID берётся из URL."""
    try:

        entity = db.query(Entity).filter(Entity.id == id).first() # Запрос
        db.delete(entity)
        db.commit()
        logger.info(f'Data deleted for id: {entity.id}')
        return Response.from_orm(entity)
    except Exception as e:
        db.rollback()
        logger.error("Error deleteing entity: "+str(e))
        raise HTTPException(status_code=404, detail="Пользователь не удален")
