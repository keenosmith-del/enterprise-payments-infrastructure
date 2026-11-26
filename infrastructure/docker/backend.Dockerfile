FROM python:3.14-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PYTHONPATH=/app
COPY requirements.lock /app/requirements.lock
RUN pip install --no-cache-dir --require-hashes -r requirements.lock && useradd -m -u 10001 epi
COPY packages /app/packages
COPY apps /app/apps
COPY scripts/m01 /app/scripts/m01
COPY services /app/services
USER epi
ARG APP_NAME
ENV EPI_APP_NAME=${APP_NAME}
CMD ["sh", "-c", "exec uvicorn main:app --app-dir /app/apps/$EPI_APP_NAME/backend --host 0.0.0.0 --port 8000"]
