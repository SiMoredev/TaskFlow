from logging.config import fileConfig
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.db.base import Base  # импортируем Base, где наши модели

# Настройка логирования
config = context.config
fileConfig(config.config_file_name)

target_metadata = Base.metadata

# Асинхронный движок
def get_async_engine():
    return create_async_engine(config.get_main_option("sqlalchemy.url"))

# Функция для синхронного запуска (по умолчанию Alembic использует sync)
def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

# Асинхронная функция для онлайн-режима
async def run_migrations_online():
    connectable = get_async_engine()

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()

# Внутренняя синхронная функция, вызываемая через run_sync
def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata
    )

    with context.begin_transaction():
        context.run_migrations()

# Запуск миграций
if context.is_offline_mode():
    run_migrations_offline()
else:
    import asyncio
    asyncio.run(run_migrations_online())