# backend/Dockerfile
FROM python:3.12-alpine3.20

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt


# Copie du reste de l'application
COPY ./app /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
