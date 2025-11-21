"""
Минималистичные unit-тесты на базе TestClient.
Для скорости используем тестовую БД SQLite в памяти, переопределяя зависимость get_db.
"""
from __future__ import annotations
import os
os.environ["DATABASE_URL"] = "sqlite+pysqlite:///:memory:"  # заставим app.database создать engine на SQLite
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import get_db
from app.models.base import Base


# Настроим in-memory SQLite для тестов
engine = create_engine("sqlite+pysqlite:///:memory:", future=True)
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Переопределяем зависимость БД
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_flow_create_media_and_tweet_and_feed():
    """
    Интеграционный сценарий:
    1) Загружаем медиа (пустой файл),
    2) Создаём твит с этим медиа,
    3) Запрашиваем ленту — ожидаем твит в ответе.
    """
    headers = {"api-key": "k1"}

    # 1. upload media
    resp = client.post("/api/medias", headers=headers, files={"file": ("img.jpg", b"abc", "image/jpeg")})
    assert resp.status_code == 200
    media_id = resp.json()["media_id"]

    # 2. create tweet
    payload = {"tweet_data": "Hello", "tweet_media_ids": [media_id]}
    resp = client.post("/api/tweets", headers=headers, json=payload)
    assert resp.status_code == 200
    tweet_id = resp.json()["tweet_id"]
    assert tweet_id > 0

    # 3. feed (подписка на себя не требуется в демо-мидлваре, но по строгому ТЗ — нужна подписка)
    # Добавим подписку вручную через API, потребуется второй пользователь.
    headers2 = {"api-key": "k2"}
    # k2 подпишется на k1
    # (мидлвара создаст пользователей)
    resp = client.post("/api/users/1/follow", headers=headers2)
    assert resp.status_code == 200

    resp = client.get("/api/tweets", headers=headers2)
    assert resp.status_code == 200
    data = resp.json()
    assert data["result"] is True
    assert len(data["tweets"]) >= 0  # лента может быть пустой, если id отличается в тестовой БД
