FROM python:3.12-slim
WORKDIR /app
RUN pip install --no-cache-dir fastapi>=0.115 uvicorn>=0.30
COPY src ./src
ENV PYTHONPATH=/app/src
EXPOSE 8000
CMD ["uvicorn", "sitewise_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
