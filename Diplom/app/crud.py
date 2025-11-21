"""
Слой CRUD (доступ к данным).
Содержит операции над пользователями, твитами, медиа, лайками и подписками.
"""
from __future__ import annotations

from typing import Iterable

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.tweet import Tweet, Media, Like, TweetMedia
from app.models.follow import Follow


# ---- Пользователи ----
def get_user_by_id(db: Session, user_id: int) -> User | None:
    """Найти пользователя по id."""
    return db.get(User, user_id)


def get_or_create_user_by_api_key(db: Session, api_key: str, name: str = "Demo User") -> User:
    """
    Для удобства локальной демонстрации: создаёт пользователя, если его нет.
    В реальном проде пользователи создаются вне нашего сервиса.
    """
    user = db.query(User).filter(User.api_key == api_key).first()
    if user:
        return user
    user = User(name=name, api_key=api_key)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# ---- Медиа ----
def create_media(db: Session, path: str) -> Media:
    """Создать медиа запись."""
    media = Media(path=path)
    db.add(media)
    db.commit()
    db.refresh(media)
    return media


def get_medias_by_ids(db: Session, ids: Iterable[int]) -> list[Media]:
    """Получить список медиа по id."""
    return db.query(Media).filter(Media.id.in_(list(ids))).all()


# ---- Твиты ----
def create_tweet(db: Session, author_id: int, content: str, media_ids: list[int] | None) -> Tweet:
    """Создать твит с опциональными медиаприложениями."""
    tweet = Tweet(author_id=author_id, content=content)
    db.add(tweet)
    db.flush()  # получим tweet.id без commit

    if media_ids:
        medias = get_medias_by_ids(db, media_ids)
        for m in medias:
            db.add(TweetMedia(tweet_id=tweet.id, media_id=m.id))

    db.commit()
    db.refresh(tweet)
    return tweet


def delete_tweet(db: Session, tweet_id: int, author_id: int) -> bool:
    """Удалить твит, проверив, что это твит автора."""
    tweet = db.get(Tweet, tweet_id)
    if not tweet or tweet.author_id != author_id:
        return False
    db.delete(tweet)
    db.commit()
    return True


# ---- Лайки ----
def like_tweet(db: Session, user_id: int, tweet_id: int) -> None:
    """Поставить лайк (idempotent)."""
    exists = db.query(Like).filter(Like.user_id == user_id, Like.tweet_id == tweet_id).first()
    if exists:
        return
    db.add(Like(user_id=user_id, tweet_id=tweet_id))
    db.commit()


def unlike_tweet(db: Session, user_id: int, tweet_id: int) -> None:
    """Убрать лайк (idempotent)."""
    like = db.query(Like).filter(Like.user_id == user_id, Like.tweet_id == tweet_id).first()
    if like:
        db.delete(like)
        db.commit()


# ---- Подписки ----
def follow_user(db: Session, follower_id: int, followee_id: int) -> None:
    """Подписаться (idempotent)."""
    if follower_id == followee_id:
        return
    exists = db.query(Follow).filter(
        Follow.follower_id == follower_id, Follow.followee_id == followee_id
    ).first()
    if exists:
        return
    db.add(Follow(follower_id=follower_id, followee_id=followee_id))
    db.commit()


def unfollow_user(db: Session, follower_id: int, followee_id: int) -> None:
    """Отписаться (idempotent)."""
    rel = db.query(Follow).filter(
        Follow.follower_id == follower_id, Follow.followee_id == followee_id
    ).first()
    if rel:
        db.delete(rel)
        db.commit()


# ---- Лента ----
def get_feed_for_user_sorted_by_popularity(db: Session, user_id: int) -> list[Tweet]:
    """
    Получить ленту твитов от тех, на кого подписан user_id, отсортированную по популярности (кол-во лайков DESC).
    При равенстве лайков — по дате создания DESC.
    """
    sub_followees = select(Follow.followee_id).where(Follow.follower_id == user_id).subquery()

    stmt = (
        select(Tweet, func.count(Like.user_id).label("likes_count"))
        .outerjoin(Like, Like.tweet_id == Tweet.id)
        .where(Tweet.author_id.in_(select(sub_followees)))
        .group_by(Tweet.id)
        .order_by(func.count(Like.user_id).desc(), Tweet.created_at.desc())
    )
    rows = db.execute(stmt).all()
    return [row[0] for row in rows]


def get_likes_for_tweet(db: Session, tweet_id: int) -> list[tuple[int, str]]:
    """Вернуть список (user_id, name) тех, кто лайкнул твит."""
    stmt = (
        select(User.id, User.name)
        .join(Like, Like.user_id == User.id)
        .where(Like.tweet_id == tweet_id)
        .order_by(User.id.asc())
    )
    return list(db.execute(stmt).all())
