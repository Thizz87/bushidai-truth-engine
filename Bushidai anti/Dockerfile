FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install flask requests
EXPOSE 5010
CMD ["python", "bushidai_anti_digitaltwin.py"]
