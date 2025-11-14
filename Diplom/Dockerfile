FROM python:3.12-slim

WORKDIR /app
COPY pyproject.toml poetry.lock* /app/

RUN pip install --no-cache-dir poetry==1.8.3 && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --only main

COPY app /app/app
COPY alembic /app/alembic
COPY alembic.ini /app/alembic.ini

# создаём директорию для медиа
RUN mkdir -p /app/media

CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
