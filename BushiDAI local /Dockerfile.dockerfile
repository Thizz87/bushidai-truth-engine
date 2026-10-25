# Dockerfile
# Streamlit-app voor BushiDAI

FROM python:3.11-slim

WORKDIR /app

# Dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App bestanden
COPY app.py .
COPY bushidai_local_client.py .
COPY bushidai_config.yaml .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]
