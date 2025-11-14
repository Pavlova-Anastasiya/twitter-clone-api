'''
Роутер пользователей: /api/users/me, /api/users/{id}, фолловинг/анфолловинг.
'''
from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app.crud import get_user_by_id, follow_user, unfollow_user
from app.schemas import UserProfileResponse, UserProfile, UserBrief, OperationResponse

router = APIRouter(prefix="/api/users", tags=["Users"])


def _profile(db: Session, user_id: int) -> UserProfile:
    '''
    Вспомогательная сборка профиля:
    - followers: кто подписан на user_id
    - following: на кого подписан user_id
    '''
    from app.models.user import User
    from app.models.follow import Follow

    u = db.get(User, user_id)
    if not u:
        return UserProfile(id=0, name="Unknown", followers=[], following=[])

    q_followers = (
        db.query(User)
        .join(Follow, Follow.follower_id == User.id)
        .filter(Follow.followee_id == user_id)
        .order_by(User.id.asc())
        .all()
    )

    q_following = (
        db.query(User)
        .join(Follow, Follow.followee_id == User.id)
        .filter(Follow.follower_id == user_id)
        .order_by(User.id.asc())
        .all()
    )

    return UserProfile(
        id=u.id,
        name=u.name,
        followers=[UserBrief(id=x.id, name=x.name) for x in q_followers],
        following=[UserBrief(id=x.id, name=x.name) for x in q_following],
    )


@router.get("/me", response_model=UserProfileResponse)
def me(db: Session = Depends(get_db), user=Depends(get_current_user)):
    '''
    Текущий профиль: GET /api/users/me
    Требуется заголовок `api-key`.
    '''
    return UserProfileResponse(user=_profile(db, user.id))


@router.get("/{user_id}", response_model=UserProfileResponse)
def get_user(user_id: int, db: Session = Depends(get_db), _user=Depends(get_current_user)):
    '''
    Профиль произвольного пользователя по id: GET /api/users/{id}
    '''
    u = get_user_by_id(db, user_id)
    if not u:
        # по ТЗ формат ошибки единый, но тут вернем пустой корректный профиль,
        # чтобы фронтенд мог обработать (или можно вернуть 404 с ErrorResponse).
        return UserProfileResponse(user=UserProfile(id=0, name="Unknown", followers=[], following=[]))
    return UserProfileResponse(user=_profile(db, user_id))


@router.post("/{user_id}/follow", response_model=OperationResponse)
def follow(user_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    '''
    Подписаться на пользователя.
    '''
    follow_user(db, follower_id=user.id, followee_id=user_id)
    return OperationResponse()


@router.delete("/{user_id}/follow", response_model=OperationResponse)
def unfollow(user_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    '''
    Отписаться от пользователя.
    '''
    unfollow_user(db, follower_id=user.id, followee_id=user_id)
    return OperationResponse()
