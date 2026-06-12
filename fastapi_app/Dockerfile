FROM python:3.11.6-slim
WORKDIR /bot
COPY requirements.txt ./

# RUN apt install libpq-dev gcc

RUN pip install -r requirements.txt

COPY . ./


EXPOSE 8000

# CMD ["python", "main.py"] 
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
