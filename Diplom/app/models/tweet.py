'''
ORM-модель твита и связей: медиа, лайки.
'''
from __future__ import annotations

from datetime import datetime

from sqlalchemy import ForeignKey, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Tweet(Base):
    '''
    Твит (сообщение).

    Поля:
        id: PK.
        author_id: автор (FK users.id).
        content: текст твита.
        created_at: дата создания (серверное NOW()).

    Связи:
        author: User.
        medias: список Media через таблицу tweet_medias.
        likes: список Like.
    '''
    __tablename__ = "tweets"

    id: Mapped[int] = mapped_column(primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    author = relationship("User", back_populates="tweets")
    medias = relationship("Media", secondary="tweet_medias", back_populates="tweets")
    likes = relationship("Like", back_populates="tweet", cascade="all, delete-orphan")


class Media(Base):
    '''
    Медиа-файл, загруженный пользователем.

    Поля:
        id: PK.
        path: относительный путь к файлу.
        created_at: дата загрузки.
    '''
    __tablename__ = "medias"

    id: Mapped[int] = mapped_column(primary_key=True)
    path: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    tweets = relationship("Tweet", secondary="tweet_medias", back_populates="medias")


class TweetMedia(Base):
    '''
    Связующая таблица "многие-ко-многим" между твитами и медиа-файлами.
    '''
    __tablename__ = "tweet_medias"

    tweet_id: Mapped[int] = mapped_column(ForeignKey("tweets.id", ondelete="CASCADE"), primary_key=True)
    media_id: Mapped[int] = mapped_column(ForeignKey("medias.id", ondelete="CASCADE"), primary_key=True)


class Like(Base):
    '''
    Лайк твита пользователем (составной PK).
    '''
    __tablename__ = "likes"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    tweet_id: Mapped[int] = mapped_column(ForeignKey("tweets.id", ondelete="CASCADE"), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    tweet = relationship("Tweet", back_populates="likes")
