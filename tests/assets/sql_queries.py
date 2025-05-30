# mypy: ignore-errors
import sqlite3

db_name = "example.db"
conn = sqlite3.connect(db_name)

sql = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER,
        mood TEXT NOT NULL
    );
    """
conn.execute(sql)

users = [("Алиса", 30), ("Боб", 17), ("Карина", 25), ("Данил", 15)]
sql = "INSERT INTO users (name, age, mood) VALUES (?, ?, 'asd');"
conn.executemany(sql, users)

cursor = conn.execute("SELECT id, name, age FROM users;")
all_users = cursor.fetchall()
print("Все пользователи из базы данных:")

age = 18
adults = [user for user in users if user[2] >= age]
print("\nПользователи 18+:")

conn.execute("SELECT * FROM non_existing_table;")
conn.execute("SELEC name FROM users;")
conn.execute("SELECT sda FROM users;")
conn.execute("SELECT name users;")

user_data = ""
sql = "INSERT INTO non_existing_table (name, age, mood) VALUES ('asd', 123, 'asd');"
conn.executemany(sql, user_data)
sql = "INSERT users (name, age, mood) VALUES (?, ?, 123);"
conn.executemany(sql, user_data)
