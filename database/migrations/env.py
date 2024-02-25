import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

from database.base import Base
from database.models import PetType, SocialNetworkType
from settings import settings

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
postgres_dsn = f'postgresql+asyncpg://{settings.postgres_user}:{settings.postgres_password}@postgres:5432/{settings.postgres_db}'
config.set_main_option('sqlalchemy.url', postgres_dsn)


# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def insert_default_pet_types(connectable):
    default_pet_types = [
        {'id': 0, 'name': 'Кошка'},
        {'id': 1, 'name': 'Собака'},
        {'id': 2, 'name': 'Грызун'},
        {'id': 3, 'name': 'Птица'},
        {'id': 4, 'name': 'Экзотическое'},
    ]

    async with connectable.connect() as connection:
        stmt = insert(PetType).on_conflict_do_nothing().values(default_pet_types)
        await connection.execute(stmt)
        await connection.commit()
        

async def insert_default_social_network_types(connectable):
    default_social_network_types = [
        {'id': 0, 'name': 'Telegram'},
        {'id': 1, 'name': 'VK'},
    ]

    async with connectable.connect() as connection:
        stmt = insert(SocialNetworkType).on_conflict_do_nothing().values(default_social_network_types)
        await connection.execute(stmt)
        await connection.commit()


async def run_async_migrations() -> None:
    """In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await insert_default_pet_types(connectable)
    await insert_default_social_network_types(connectable)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""

    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
