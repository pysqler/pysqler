import pytest
import sqlite3

from  pysqler.providers import _sqlite3



sql = ["CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)",
"CREATE TABLE users1 (id INTEGER PRIMARY KEY, surname TEXT, age INTEGER)",
"CREATE TABLE users2 (id INTEGER PRIMARY KEY, balance INTEGER)"]


# фикстура
@pytest.fixture
def conn():
    # setup: создаём подключение
    conn = sqlite3.connect('')
    conn.commit()

    yield conn  # передаём объект тесту

    # teardown: закрываем соединение
    conn.close()


def test_fetches_valid_schema(conn) -> None:
    cursor = conn.cursor()
    for table in sql:
        cursor.execute(table)

    assert _sqlite3.extract_schema(conn) == sql