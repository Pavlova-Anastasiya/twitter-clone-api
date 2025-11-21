"""
Конфигурация приложения.
Читает переменные окружения и предоставляет значения для остальных модулей.
"""
from __future__ import annotations

import os


class Settings:
    """
    Класс настроек.

    Атрибуты:
        database_url: строка подключения SQLAlchemy.
        api_title: заголовок OpenAPI/Swagger.
        api_version: версия API.
        media_dir: директория хранения загруженных файлов.
    """
    database_url: str = os.getenv("DATABASE_URL", "postgresql+psycopg://microblog:microblog@localhost:5432/microblog")
    api_title: str = os.getenv("API_TITLE", "Microblog Service")
    api_version: str = os.getenv("API_VERSION", "1.0.0")
    media_dir: str = os.getenv("MEDIA_DIR", "media")


settings = Settings()
