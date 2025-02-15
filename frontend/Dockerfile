# frontend/Dockerfile
FROM python:3.12-alpine3.20

WORKDIR /app

COPY requirements.txt .
RUN pip install  -r requirements.txt

COPY . .

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
