# frontend/Dockerfile
FROM python:3.10-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install  -r requirements.txt

COPY . .

CMD ["streamlit", "run", "pages/patient.py", "--server.port=8501", "--server.address=0.0.0.0"]
