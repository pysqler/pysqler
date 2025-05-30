import sqlite3
from sqlite3 import Connection
from typing import Any

from pysqler.parser import SqlFieldsTypes, TableName, extract_schema_types


def extract_schema(conn: Connection) -> dict[TableName, SqlFieldsTypes]:
    cursor = conn.cursor()
    cursor.execute("SELECT sql FROM sqlite_master WHERE sql IS NOT NULL")
    schema_entries = cursor.fetchall()
    schema = ";".join(entry[0] for entry in schema_entries if entry[0])
    return extract_schema_types(schema)


def mock_db(schema: list[str]) -> Connection:
    conn = sqlite3.connect("")
    cursor = conn.cursor()

    for table in schema:
        cursor.execute(table)
    conn.commit()
    return conn


def execute(conn: Connection, query: str, args: tuple[Any, ...]) -> None:
    print(f"{query=}")
    cursor = conn.cursor()
    cursor.execute(query, args)
    conn.rollback()


def to_python_type(sqlite_type: str) -> type:
    sqlite_type = sqlite_type.strip().upper()

    if "INT" in sqlite_type:
        return int
    if "CHAR" in sqlite_type or "CLOB" in sqlite_type or "TEXT" in sqlite_type:
        return str
    if "BLOB" in sqlite_type:
        return bytes
    if (
        "REAL" in sqlite_type
        or "FLOA" in sqlite_type
        or "DOUB" in sqlite_type
        or "NUMERIC" in sqlite_type
        or "DECIMAL" in sqlite_type
    ):
        return float
    if sqlite_type == "NULL":
        return type(None)
    return str
