import sqlite3
from collections.abc import Generator

import pytest

from pysqler.providers import _sqlite3

sql = [
    "CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)",
    "CREATE TABLE users1 (id INTEGER PRIMARY KEY, surname TEXT, age INTEGER)",
    "CREATE TABLE users2 (id INTEGER PRIMARY KEY, balance INTEGER)",
]


@pytest.fixture
def conn() -> Generator[sqlite3.Connection]:
    conn = sqlite3.connect("")
    yield conn
    conn.close()


def test_fetches_valid_schema(conn: sqlite3.Connection) -> None:
    cursor = conn.cursor()
    for table in sql:
        cursor.execute(table)
    expected = {
        "users": {"id": "INTEGER", "name": "TEXT", "age": "INTEGER"},
        "users1": {"id": "INTEGER", "surname": "TEXT", "age": "INTEGER"},
        "users2": {"id": "INTEGER", "balance": "INTEGER"},
    }
    assert _sqlite3.extract_schema(conn) == expected
