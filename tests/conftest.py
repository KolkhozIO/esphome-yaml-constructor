import os
import sys
from typing import Generator, Any

import pytest
from jose import jwt
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import settings

from db.connect import get_db
from main import app
import asyncio
import asyncpg

CLEAN_TABLES = [
    "config",
    "users",
    "user_config"
]

TEST_DATABASE_URL = os.environ.get("SQLALCHEMY_DATABASE_POSTGRES_URL")


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def run_migrations():
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


def get_file_name(data_from_resp):
    start_text = "./uploaded_files/"
    end_text = ".yaml"

    start_index = data_from_resp.find(start_text) + len(start_text)
    end_index = data_from_resp.find(end_text, start_index)

    extracted_content = data_from_resp[start_index:end_index]
    return extracted_content


async def decode_test_token(access_token):
    payload = jwt.decode(
        access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )
    email: str = payload.get("sub")
    return email