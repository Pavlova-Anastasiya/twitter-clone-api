'''
Зависимости FastAPI: авторизация по заголовку api-key.
'''
from __future__ import annotations

from fastapi import Header, HTTPException, status, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User


def get_current_user(
    db: Session = Depends(get_db),
    api_key: str | None = Header(default=None, alias="api-key"),
) -> User:
    '''
    Возвращает текущего пользователя по заголовку `api-key`.

    Исключения:
        401, если заголовок отсутствует или пользователь не найден.
    '''
    if not api_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing api-key header")
    user = db.query(User).filter(User.api_key == api_key).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid api-key")
    return user
