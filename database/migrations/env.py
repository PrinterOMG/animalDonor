import asyncio
import datetime
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

from database.base import Base
from database.models import PetType, Pet, User, SearchCard
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


async def insert_presentation_user(connectable):
    data_list = [
        {
            "first_name": "Иван",
            "second_name": "Иванов",
            "patronymic": "Иванович",
            "email": "ivan@example.com",
            "hashed_password": "$2b$12$h1IstOesIQ26GC5xG3caDeVxp/yP0U0YBi7DVdAZxuB3aJwOWEOqO",  # password
            "is_active": True,
            "city": "Москва",
            "is_email_public": False,
            "created_at": datetime.datetime.utcnow(),
            "phone": "79101234567",
            "is_email_confirm": True,
            "telegram_id": None
        },
        {
            "first_name": "Мария",
            "second_name": "Петрова",
            "patronymic": "Сергеевна",
            "email": "maria@example.com",
            "hashed_password": "$2b$12$h1IstOesIQ26GC5xG3caDeVxp/yP0U0YBi7DVdAZxuB3aJwOWEOqO",
            "is_active": True,
            "city": "Санкт-Петербург",
            "is_email_public": True,
            "created_at": datetime.datetime.utcnow(),
            "phone": "79998765432",
            "is_email_confirm": True,
            "telegram_id": None
        }
    ]

    async with connectable.connect() as connection:
        stmt = insert(User).on_conflict_do_nothing().values(data_list)
        await connection.execute(stmt)
        await connection.commit()


async def insert_presentation_pets(connectable):
    data_list = [
        {
            "name": "Пушистик",
            "breed": "Персидская",
            "blood_type": "A",
            "birthday": datetime.date(2019, 5, 15),
            "weight": 4.5,
            "created_at": datetime.datetime(2023, 7, 10, 8, 30),
            "role": "Донор",
            "owner_id": 1,
            "pet_type_id": 0
        },
        {
            "name": "Шарик",
            "breed": "Золотистый ретривер",
            "blood_type": "DEA1-",
            "birthday": datetime.date(2020, 3, 20),
            "weight": 30.2,
            "created_at": datetime.datetime(2023, 9, 5, 11, 45),
            "role": "Донор",
            "owner_id": 1,
            "pet_type_id": 1
        },
        {
            "name": "Барсик",
            "breed": "Сиамская",
            "blood_type": "A",
            "birthday": datetime.date(2022, 1, 3),
            "weight": 3.1,
            "created_at": datetime.datetime(2024, 1, 20, 10, 15),
            "role": "Реципиент",
            "owner_id": 2,
            "pet_type_id": 0
        }
    ]

    async with connectable.connect() as connection:
        stmt = insert(Pet).on_conflict_do_nothing().values(data_list)
        await connection.execute(stmt)
        await connection.commit()


async def insert_presentation_search_card(connectable):
    data_list = [
        {
            "description": "Срочно нужна кровь для переливания. Помогите Пушистику",
            "destination_point": "Городская ветеринарная клиника",
            "blood_amount": 50,
            "active_until": datetime.date(2024, 3, 1),
            "is_active": True,
            "created_at": datetime.datetime.utcnow(),
            "author_id": 1,
            "recipient_id": 1
        },
        {
            "description": "Ищем донора крови для нашего питомца",
            "destination_point": "Домашний ветеринар",
            "blood_amount": 150,
            "active_until": datetime.date(2024, 2, 28),
            "is_active": True,
            "created_at": datetime.datetime.utcnow(),
            "author_id": 2,
            "recipient_id": 2
        }
    ]

    async with connectable.connect() as connection:
        stmt = insert(SearchCard).on_conflict_do_nothing().values(data_list)
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

    presentation = True

    if presentation:
        await insert_presentation_user(connectable)
        await insert_presentation_pets(connectable)
        await insert_presentation_search_card(connectable)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""

    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
