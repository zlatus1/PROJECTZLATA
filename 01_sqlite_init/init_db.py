
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "app.db"


def main() -> None:
    connection = sqlite3.connect(DB_PATH)
    try:
        cursor = connection.cursor()
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                status TEXT DEFAULT 'new'
            )"""
        )
        connection.commit()
        print("База данных и таблица tasks успешно созданы.")
    finally:
        connection.close()


if __name__ == "__main__":
    main()
