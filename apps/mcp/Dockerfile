FROM python:3.12-slim
WORKDIR /app
RUN pip install --no-cache-dir fastapi>=0.115 uvicorn>=0.30
COPY src ./src
ENV PYTHONPATH=/app/src
EXPOSE 8001
CMD ["uvicorn", "sitewise_mcp.server:app", "--host", "0.0.0.0", "--port", "8001"]
