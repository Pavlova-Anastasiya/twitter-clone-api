'''
Подключение к базе данных и сессия SQLAlchemy.
Создаёт engine и sessionmaker, предоставляет зависимость get_db() для FastAPI.
'''
from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings

engine = create_engine(settings.database_url, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def get_db():
    '''
    Зависимость FastAPI: даёт транзакционную сессию БД на время запроса.
    Гарантирует закрытие сессии.
    '''
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
