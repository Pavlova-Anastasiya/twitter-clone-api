"""
Точка входа FastAPI-приложения.

Возможности:
- Swagger UI/OpenAPI по адресу /docs и /openapi.json;
- Роутеры для users, tweets, medias;
- Поддержка заголовка `api-key` (для фронтенда и Swagger), но БЕЗ проверки на бэкенде;
- Демонстрационный хук старта: создаёт пользователей по api-key из заголовка при первом обращении.
"""
from __future__ import annotations

from typing import Optional

from fastapi import FastAPI, Request, Security
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.crud import get_or_create_user_by_api_key
from app.routers import users, tweets, medias
from fastapi.openapi.utils import get_openapi


# --- Заголовок api-key для Swagger и фронтенда ---
# ВАЖНО: проверку ключа на бэке мы НЕ делаем, как просил куратор.
api_key_header = APIKeyHeader(
    name="api-key",
    description="Ключ, который проверяет только фронтенд (например: test).",
    auto_error=False,
)


def require_api_key(api_key: Optional[str] = Security(api_key_header)) -> str:
    """
    В итоговом проекте Python Advanced бэкенд НЕ проверяет значение api-key.
    Наличие/значение ключа проверяет только фронтенд.

    Функция оставлена только для того, чтобы в Swagger была кнопка Authorize
    и можно было удобно подставлять заголовок api-key при тестировании.
    """
    # Никаких HTTPException здесь НЕ бросаем.
    return api_key or "anonymous"


# Приложение
app = FastAPI(title=settings.api_title, version=settings.api_version)

# Подключаем роутеры.
# dependencies=[Security(require_api_key)] оставляем только ради схемы в Swagger,
# фактической проверки внутри require_api_key больше нет.
app.include_router(medias.router, prefix="/api", dependencies=[Security(require_api_key)])
app.include_router(tweets.router, prefix="/api", dependencies=[Security(require_api_key)])
app.include_router(users.router,  prefix="/api", dependencies=[Security(require_api_key)])


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        routes=app.routes,
        description="Microblog Service",
    )
    # схема авторизации через apiKey в заголовке
    openapi_schema.setdefault("components", {}).setdefault("securitySchemes", {})["ApiKeyAuth"] = {
        "type": "apiKey",
        "in": "header",
        "name": "api-key",
    }
    # глобальная “подсказка” про авторизацию (не делает заголовок обязательным)
    openapi_schema["security"] = [{"ApiKeyAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


# ВАЖНО: обработчик корня "/" УДАЛЁН.
# Раздачей статики (index.html) занимается nginx, как написал куратор.
# Поэтому здесь НИКАКИХ @app.get("/") быть не должно.


@app.middleware("http")
async def demo_autocreate_user(request: Request, call_next):
    """
    Демонстрационная прослойка: если приходит заголовок `api-key`,
    а такого пользователя ещё нет — создаём его с именем "User <last 6>".
    Бэкенд при этом НИЧЕГО не валидирует.
    """
    api_key = request.headers.get("api-key")
    if api_key:
        short = api_key[-6:]
        db: Session | None = None
        try:
            db = next(get_db())
            get_or_create_user_by_api_key(db, api_key=api_key, name=f"User {short}")
        finally:
            if db:
                db.close()
    return await call_next(request)
