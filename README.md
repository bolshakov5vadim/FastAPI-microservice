Скачать - wget https://github.com/bolshakov5vadim/FastAPI-microservice/archive/main.zip
unzip main.zip

В e.env записать адрес БД

sudo docker build . -t fastapi_app

sudo docker run -p 8000:8000 fastapi_app