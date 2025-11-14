'''
ORM-модель пользователя.
Содержит имя и уникальный api_key для заголовка `api-key`.
'''
from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class User(Base):
    '''
    Модель пользователя.

    Поля:
        id: PK.
        name: отображаемое имя.
        api_key: уникальный ключ для заголовка авторизации (api-key).
    '''
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    api_key: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)

    tweets = relationship("Tweet", back_populates="author", cascade="all, delete-orphan")
