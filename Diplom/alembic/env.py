"""
Модуль Alembic env.
Настраивает контекст миграций, подхватывает DATABASE_URL из переменных окружения,
подключает метаданные моделей для автогенерации (autogenerate).

Ключевые моменты:
- offline/online режимы миграций;
- интеграция с моделями (app.models.base.Base.metadata).
"""
from __future__ import annotations

import os
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from app.models.base import Base  # noqa: F401 - для target_metadata

# Подключаем конфиг и логирование
config = context.config
fileConfig(config.config_file_name)

# Перекладываем DATABASE_URL из окружения в конфиг Alembic
db_url = os.getenv("DATABASE_URL")
if db_url:
    config.set_main_option("sqlalchemy.url", db_url)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """
    Запуск миграций в offline-режиме (без реального подключения к БД).
    Генерирует SQL-скрипты.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    Запуск миграций в online-режиме (с подключением к БД).
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        future=True,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
