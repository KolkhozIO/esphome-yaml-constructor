import os
import sys
import uuid
from typing import Generator, Any

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from db.connect import get_db
from main import app
import asyncio
import asyncpg

TEST_DATABASE_URL = (
    "postgresql+asyncpg://testkolkhoz:testkolkhoz@test-db:5432/testkolkhoz"
)

CLEAN_TABLES = [
    "config",
    "users",
    "user_config"
]


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def run_migrations():
    os.system("alembic init migrations")
    os.system('alembic revision --autogenerate -m "test running migrations"')
    os.system("alembic upgrade heads")


@pytest.fixture(scope="session")
async def async_session_test():
    engine = create_async_engine(TEST_DATABASE_URL, future=True, echo=True)
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    yield async_session


@pytest.fixture(scope="function", autouse=True)
async def clean_tables(async_session_test):
    """Clean data in all tables before running test function"""
    async with async_session_test() as session:
        async with session.begin():
            for table_for_cleaning in CLEAN_TABLES:
                await session.execute(text(f"TRUNCATE TABLE {table_for_cleaning} CASCADE;"))


async def _get_test_db():
    try:
        # create async engine for interaction with database
        test_engine = create_async_engine(
            TEST_DATABASE_URL, future=True, echo=True
        )

        # create session for the interaction with database
        test_async_session = sessionmaker(
            test_engine, expire_on_commit=False, class_=AsyncSession
        )
        yield test_async_session()
    finally:
        pass


@pytest.fixture(scope="function")
async def client() -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture to override
    the `get_db` dependency that is injected into routes.
    """

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="session")
async def asyncpg_pool():
    pool = await asyncpg.create_pool(
        "".join(TEST_DATABASE_URL.split("+asyncpg"))
    )
    yield pool
    pool.close()


@pytest.fixture
async def get_config_from_database(asyncpg_pool):
    async def get_config_from_database_by_name_config(name_config: uuid):
        async with asyncpg_pool.acquire() as connection:
            return await connection.fetch("SELECT * FROM config WHERE name_config = $1;", name_config)

    return get_config_from_database_by_name_config


@pytest.fixture
async def get_config_by_config_json(asyncpg_pool):
    async def get_config_from_database_by_config_json(config_json: str):
        async with asyncpg_pool.acquire() as connection:
            return await connection.fetch("SELECT * FROM config WHERE config_json = $1;", config_json)

    return get_config_from_database_by_config_json


@pytest.fixture
async def create_config_in_database(asyncpg_pool):
    async def create_config_in_database(
            name_config: uuid.UUID,
            hash_yaml: str,
            compile_test: bool,
            name_esphome: str,
            platform: str,
            config_json: str
    ):
        async with asyncpg_pool.acquire() as connection:
            return await connection.execute(
                """INSERT INTO config VALUES ($1, $2, $3, $4, $5, $6)""",
                name_config,
                hash_yaml,
                compile_test,
                name_esphome,
                platform,
                config_json,
            )

    return create_config_in_database


@pytest.fixture
async def get_user_from_database(asyncpg_pool):
    async def get_user_from_database(email: str):
        async with asyncpg_pool.acquire() as connection:
            return await connection.fetch("SELECT * FROM users WHERE email = $1;", email)

    return get_user_from_database


@pytest.fixture
async def get_user_from_database_by_user_id(asyncpg_pool):
    async def get_user_from_database(user_id: str):
        async with asyncpg_pool.acquire() as connection:
            return await connection.fetch("SELECT * FROM users WHERE user_id = $1;", user_id)

    return get_user_from_database


@pytest.fixture
async def get_favourites_from_database(asyncpg_pool):
    async def get_favourites_from_database(id: int):
        async with asyncpg_pool.acquire() as connection:
            return await connection.fetch("SELECT * FROM user_config WHERE id = $1;", id)

    return get_favourites_from_database


@pytest.fixture
async def get_favourites_from_database_by_user_id(asyncpg_pool):
    async def get_favourites_from_database_by_user_id(user_id: str):
        async with asyncpg_pool.acquire() as connection:
            return await connection.fetch("SELECT * FROM user_config WHERE user_id = $1;", user_id)

    return get_favourites_from_database_by_user_id


@pytest.fixture
async def create_favourites_in_database(asyncpg_pool):
    async def create_favourites_in_database(
            id: int,
            user_id: str,
            name_config: uuid.UUID,
            name_esphome: str,
    ):
        async with asyncpg_pool.acquire() as connection:
            await connection.execute(
                """INSERT INTO user_config VALUES ($1, $2, $3, $4)""",
                id,
                user_id,
                name_config,
                name_esphome,
            )
            return await connection.fetch("SELECT * FROM user_config WHERE id = $1;", id)

    return create_favourites_in_database


@pytest.fixture
async def create_test_user(asyncpg_pool):
    async def create_test_user(
            user_id: str,
            name: str,
            surname: str,
            email: str,
            is_active: bool
    ):
        async with asyncpg_pool.acquire() as connection:
            await connection.execute(
                """INSERT INTO users VALUES ($1, $2, $3, $4, $5)""",
                user_id,
                name,
                surname,
                email,
                is_active,
            )
            return await connection.fetch("SELECT * FROM users WHERE email = $1;", email)

    return create_test_user


@pytest.fixture
async def create_test_config(asyncpg_pool):
    async def create_test_config(
            name_config: uuid.UUID,
            hash_yaml: str,
            compile_test: bool,
            name_esphome: str,
            platform: str,
            config_json: str
    ):
        async with asyncpg_pool.acquire() as connection:
            await connection.execute(
                """INSERT INTO config VALUES ($1, $2, $3, $4, $5, $6)""",
                name_config,
                hash_yaml,
                compile_test,
                name_esphome,
                platform,
                config_json,
            )
            return await connection.fetch("SELECT * FROM config WHERE config_json = $1;", config_json)

    return create_test_config
