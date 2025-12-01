from SQLsession import SessionLocal
from Models import Entity

from sqlalchemy.orm import Session

from fastapi import Depends, FastAPI, Body, HTTPException
from fastapi.responses import JSONResponse, FileResponse
import logging
from pydantic import BaseModel


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

    class Config:
        orm_mode = True 


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
   

# API + описание 4-х действий
app = FastAPI()


@app.get("/api", response_model = Response)
def read(data  = Body(), db: Session = Depends(get_db)):
    
    try:

        if(data["page"]): entity = db.query(Entity).limit(10).offset((data["page"] - 1) * 10).all()
        # if(data["classroom"]): entity = db.query(Entity).filter(Entity.classroom == data["classroom"])
        # Возврат похожих картинок. Вектор "classroom" будет выдаваться классификатором 
        return Response.from_orm(entity)

    except Exception as e:
        logger.info(f"Data requested for page {data["page"]}")
        raise HTTPException(status_code=404, detail="Пользователь не найден")


  
@app.post("/api", response_model = Response)
def create(data  = Body(), db: Session = Depends(get_db)):

    try:
        entity = Entity(name=data["name"], description=data["description"], likes=data["likes"])
        # Если используется auto-increment, не нужно отправлять id 

        db.add(entity)
        db.commit()
        db.refresh(entity)
        logger.info(f"Data posted")
        return Response.from_orm(entity)
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating entity: {str(e)}")
        raise HTTPException(status_code=404, detail="Пользователь не создан")

  
@app.delete("/api/{id}")
def delete(id: int, db: Session = Depends(get_db)):

    try:
        entity = db.query(Entity).filter(Entity.id == id).first() # Запрос
        db.delete(entity)
        db.commit()
        logger.info(f"Data deleted for id: {entity.id}")
        return Response.from_orm(entity)
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleteing entity: {str(e)}")
         raise HTTPException(status_code=404, detail="Пользователь не удален")