# mypy: ignore-errors
import sqlite3


def create_connection(db_name):
    return sqlite3.connect(db_name)


def create_table(conn):
    sql = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER
    );
    """
    conn.execute(sql)
    conn.commit()


def insert_users(conn, user_data):
    sql = "INSERT INTO users (name, age, mode) VALUES (?, 123, ?);"
    conn.executemany(sql, user_data)
    conn.commit()


def fetch_users(conn):
    cursor = conn.execute("SELECT id, name, age FROM users;")
    return cursor.fetchall()


def filter_adults(users):
    age = 18
    return [user for user in users if user[2] >= age]


def main():
    db_name = "example.db"
    conn = create_connection(db_name)

    create_table(conn)

    users = [("Алиса", 30), ("Боб", 17), ("Карина", 25), ("Данил", 15)]
    insert_users(conn, users)

    all_users = fetch_users(conn)
    print("Все пользователи из базы данных:")
    for user in all_users:
        print(user)

    adults = filter_adults(all_users)
    print("\nПользователи 18+:")
    for user in adults:
        print(user)

    conn.close()


if __name__ == "__main__":
    main()
