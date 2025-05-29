from sqlite3 import Connection


def extract_schema(conn: Connection) -> list[str]:
    cursor = conn.cursor()
    cursor.execute("SELECT sql FROM sqlite_master WHERE sql IS NOT NULL")
    schema_entries = cursor.fetchall()
    return [entry[0] for entry in schema_entries if entry[0]]