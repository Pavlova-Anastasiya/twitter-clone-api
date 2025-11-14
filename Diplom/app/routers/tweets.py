'''
Роутер твитов: создание, удаление, лайки, лента.
'''
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app.schemas import (
    TweetCreate,
    CreateTweetResponse,
    OperationResponse,
    TweetListResponse,
    TweetItem,
    TweetAuthor,
    TweetLikeUser,
    ErrorResponse,
)
from app.crud import create_tweet, delete_tweet, like_tweet, unlike_tweet, get_feed_for_user_sorted_by_popularity, get_likes_for_tweet

router = APIRouter(prefix="/api/tweets", tags=["Tweets"])


@router.post("", response_model=CreateTweetResponse, responses={400: {"model": ErrorResponse}})
def create_tweet_endpoint(
    payload: TweetCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    '''
    Создать новый твит.

    Вход:
        { "tweet_data": str, "tweet_media_ids": [int]? }
    Выход:
        { "result": true, "tweet_id": int }
    '''
    if not payload.tweet_data.strip():
        raise HTTPException(status_code=400, detail={"result": False, "error_type": "ValidationError", "error_message": "Empty tweet"})
    tweet = create_tweet(db, author_id=user.id, content=payload.tweet_data.strip(), media_ids=payload.tweet_media_ids)
    return CreateTweetResponse(tweet_id=tweet.id)


@router.delete("/{tweet_id}", response_model=OperationResponse, responses={403: {"model": ErrorResponse}, 404: {"model": ErrorResponse}})
def delete_tweet_endpoint(
    tweet_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    '''
    Удалить твит текущего пользователя.

    Ошибки:
        404 — твит не найден;
        403 — попытка удалить чужой твит.
    '''
    from app.models.tweet import Tweet  # локальный импорт во избежание циклов
    t = db.get(Tweet, tweet_id)
    if not t:
        raise HTTPException(status_code=404, detail={"result": False, "error_type": "NotFound", "error_message": "Tweet not found"})
    if t.author_id != user.id:
        raise HTTPException(status_code=403, detail={"result": False, "error_type": "Forbidden", "error_message": "Cannot delete others' tweets"})
    ok = delete_tweet(db, tweet_id=tweet_id, author_id=user.id)
    if not ok:
        raise HTTPException(status_code=403, detail={"result": False, "error_type": "Forbidden", "error_message": "Cannot delete tweet"})
    return OperationResponse()


@router.post("/{tweet_id}/likes", response_model=OperationResponse)
def like_tweet_endpoint(
    tweet_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    '''
    Поставить лайк твиту (idempotent).
    '''
    like_tweet(db, user_id=user.id, tweet_id=tweet_id)
    return OperationResponse()


@router.delete("/{tweet_id}/likes", response_model=OperationResponse)
def unlike_tweet_endpoint(
    tweet_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    '''
    Убрать лайк с твита (idempotent).
    '''
    unlike_tweet(db, user_id=user.id, tweet_id=tweet_id)
    return OperationResponse()


@router.get("", response_model=TweetListResponse)
def get_feed_endpoint(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    '''
    Получить ленту твитов от пользователей, на которых подписан текущий пользователь,
    отсортированную по популярности (кол-во лайков по убыванию), при равенстве — по дате.

    Формат выхода соответствует ТЗ.
    '''
    tweets = get_feed_for_user_sorted_by_popularity(db, user_id=user.id)
    items: list[TweetItem] = []
    for t in tweets:
        likes = [TweetLikeUser(user_id=uid, name=name) for uid, name in get_likes_for_tweet(db, t.id)]
        attachments = [m.path for m in t.medias]
        items.append(
            TweetItem(
                id=t.id,
                content=t.content,
                attachments=attachments,
                author=TweetAuthor(id=t.author.id, name=t.author.name),
                likes=likes,
            )
        )
    return TweetListResponse(tweets=items)
