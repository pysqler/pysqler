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

def _to_python_type(sqlite_type: str) -> type:

    sqlite_type = sqlite_type.strip().upper()

    if "INT" in sqlite_type:
        return int
    elif "CHAR" in sqlite_type or "CLOB" in sqlite_type or "TEXT" in sqlite_type:
        return str
    elif "BLOB" in sqlite_type:
        return bytes
    elif "REAL" in sqlite_type or "FLOA" in sqlite_type or "DOUB" in sqlite_type:
        return float
    elif "NUMERIC" in sqlite_type or "DECIMAL" in sqlite_type:
        return float
    elif sqlite_type == "NULL":
        return type(None)
    else:
        return str