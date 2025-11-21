"""
Pydantic-схемы запросов/ответов.
Служат валидации и формируют контракт API (Swagger).
"""
from __future__ import annotations

from typing import List, Optional
from pydantic import BaseModel, Field


# ---- Пользователи ----
class UserBrief(BaseModel):
    """Короткое представление пользователя."""
    id: int
    name: str


class UserProfile(BaseModel):
    """Профиль пользователя с фоловерами и фоловингом."""
    id: int
    name: str
    followers: List[UserBrief]
    following: List[UserBrief]


class UserProfileResponse(BaseModel):
    """Обёртка ответа с профилем."""
    result: bool = True
    user: UserProfile


# ---- Медиа ----
class MediaUploadResponse(BaseModel):
    """Ответ при успешной загрузке медиа."""
    result: bool = True
    media_id: int


# ---- Твиты ----
class TweetCreate(BaseModel):
    """Запрос на создание твита."""
    tweet_data: str = Field(..., min_length=1, description="Текст твита")
    tweet_media_ids: Optional[list[int]] = Field(default=None, description="IDs загруженных медиа")


class TweetAuthor(BaseModel):
    """Автор для ответа в ленте."""
    id: int
    name: str


class TweetLikeUser(BaseModel):
    """Кто лайкнул в ответе."""
    user_id: int
    name: str


class TweetItem(BaseModel):
    """Твит в ленте."""
    id: int
    content: str
    attachments: list[str]
    author: TweetAuthor
    likes: list[TweetLikeUser]


class TweetListResponse(BaseModel):
    """Ответ ленты твитов."""
    result: bool = True
    tweets: list[TweetItem]


class CreateTweetResponse(BaseModel):
    """Ответ на создание твита."""
    result: bool = True
    tweet_id: int


class OperationResponse(BaseModel):
    """Универсальный успешный ответ на операции."""
    result: bool = True


# ---- Ошибка ----
class ErrorResponse(BaseModel):
    """Формат ошибки по ТЗ."""
    result: bool = False
    error_type: str
    error_message: str
