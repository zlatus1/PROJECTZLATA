
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "app.db"

connection = sqlite3.connect(DB_PATH)
try:
    tables = connection.execute("SELECT name FROM sqlite_master WHERE type = ?", ("table",)).fetchall()
    print("Таблицы в базе:", tables)
    if connection.execute("SELECT 1 FROM sqlite_master WHERE name = ?", ("tasks",)).fetchone():
        print("Колонки tasks:", connection.execute("PRAGMA table_info(tasks)").fetchall())
finally:
    connection.close()
