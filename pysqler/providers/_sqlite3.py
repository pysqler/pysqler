import sqlite3
from sqlite3 import Connection


def extract_schema(conn: Connection) -> list[str]:
    cursor = conn.cursor()
    cursor.execute("SELECT sql FROM sqlite_master WHERE sql IS NOT NULL")
    schema_entries = cursor.fetchall()
    return [entry[0] for entry in schema_entries if entry[0]]


def mock_db(schema: list[str]) -> Connection:
    conn = sqlite3.connect("")
    cursor = conn.cursor()

    for table in schema:
        cursor.execute(table)
    conn.commit()
    return conn


def execute(conn: Connection, query: str) -> None:
    print(f"{query=}")
    cursor = conn.cursor()
    cursor.execute(query)
    conn.rollback()
