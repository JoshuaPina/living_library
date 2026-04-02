from __future__ import annotations

import asyncio
import os

import asyncpg
import pytest

from db_bootstrap import SCHEMA_STATEMENTS, ensure_schema_with_connection, ensure_schema_with_session


class FakeSession:
    def __init__(self) -> None:
        self.statements: list[str] = []

    async def execute(self, statement) -> None:
        self.statements.append(str(statement))


class FakeConnection:
    def __init__(self) -> None:
        self.statements: list[str] = []

    async def execute(self, statement) -> None:
        self.statements.append(statement)


def test_bootstrap_session_emits_expected_statements() -> None:
    session = FakeSession()

    asyncio.run(ensure_schema_with_session(session))

    assert len(session.statements) == len(SCHEMA_STATEMENTS)
    assert any("CREATE EXTENSION IF NOT EXISTS vector" in statement for statement in session.statements)
    assert any("CREATE TABLE IF NOT EXISTS material" in statement for statement in session.statements)
    assert any("CREATE OR REPLACE FUNCTION get_material_stats()" in statement for statement in session.statements)


def test_bootstrap_connection_emits_expected_statements() -> None:
    connection = FakeConnection()

    asyncio.run(ensure_schema_with_connection(connection))

    assert len(connection.statements) == len(SCHEMA_STATEMENTS)
    assert connection.statements[0] == "CREATE EXTENSION IF NOT EXISTS vector"
    assert any("CREATE TABLE IF NOT EXISTS text_chunk" in statement for statement in connection.statements)


async def _bootstrap_on_database(database_url: str) -> None:
    connection = await asyncpg.connect(database_url)
    try:
        await ensure_schema_with_connection(connection)

        material_table = await connection.fetchval("SELECT to_regclass('public.material')")
        assert material_table == "material"

        stats_function_exists = await connection.fetchval(
            """
            SELECT EXISTS (
                SELECT 1
                FROM pg_proc
                WHERE proname = 'get_material_stats'
            )
            """
        )
        assert stats_function_exists is True

        vector_extension_exists = await connection.fetchval(
            """
            SELECT EXISTS (
                SELECT 1
                FROM pg_extension
                WHERE extname = 'vector'
            )
            """
        )
        assert vector_extension_exists is True
    finally:
        await connection.close()


def test_bootstrap_can_run_against_real_postgres() -> None:
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        pytest.skip("DATABASE_URL is not set")

    asyncio.run(_bootstrap_on_database(database_url))
