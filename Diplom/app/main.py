"""
Точка входа FastAPI-приложения.

Возможности:
- Swagger UI/OpenAPI по адресу /docs и /openapi.json;
- Роутеры для users, tweets, medias;
- Глобальная защита API ключом через заголовок `api-key` (кнопка Authorize в Swagger);
- Простая домашняя страница со ссылкой на Swagger;
- Демонстрационный хук старта: создаёт пользователей по api-key из заголовка при первом обращении.
"""
from __future__ import annotations

import os
from typing import Optional

from fastapi import FastAPI, Request, Security, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.crud import get_or_create_user_by_api_key
from app.routers import users, tweets, medias
from fastapi.openapi.utils import get_openapi
# --- Security: схема API key для Swagger и проверка ключа ---
# Заголовок, из которого берём ключ
api_key_header = APIKeyHeader(
    name="api-key",
    description="Введите один из ключей из .env (например k1 или k2).",
    auto_error=False,
)

# Разрешённые значения ключей из .env (.env в корне проекта/compose):
# API_KEY_K1=k1
# API_KEY_K2=k2
VALID_KEYS = {os.getenv("API_KEY_K1"), os.getenv("API_KEY_K2")}
VALID_KEYS.discard(None)  # на случай, если переменная не задана


def require_api_key(api_key: Optional[str] = Security(api_key_header)) -> str:
    if not api_key or api_key not in VALID_KEYS:
        # важный момент: 401 + WWW-Authenticate, чтобы Swagger красиво реагировал
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key",
            headers={"WWW-Authenticate": "API-Key"},
        )
    return api_key


# Приложение
app = FastAPI(title=settings.api_title, version=settings.api_version)

# Подключаем роутеры и вешаем защиту на все эндпоинты этих роутеров
# (если нужно защитить не всё — убери dependencies у нужного router и ставь на отдельные ручки)
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

@app.get("/", response_class=HTMLResponse)
def index() -> str:
    """Простейшая домашняя страница c ссылкой на Swagger."""
    return """
    <html>
      <head><title>Microblog Service</title></head>
      <body>
        <h1>Microblog Service</h1>
        <p>Откройте <a href="/docs">Swagger UI</a> для тестирования API.</p>
      </body>
    </html>
    """


@app.middleware("http")
async def demo_autocreate_user(request: Request, call_next):
    """
    Демонстрационная прослойка: если приходит заголовок `api-key`,
    а такого пользователя ещё нет — создаём его с именем "User <last 6>".
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
