
import argparse

from db import DEFAULT_DB_PATH, get_connection


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspect the task manager database.")
    parser.add_argument("--db", default=str(DEFAULT_DB_PATH), help="database file path")
    args = parser.parse_args()

    connection = get_connection(args.db)
    try:
        tables = connection.execute(
            "SELECT name FROM sqlite_master WHERE type = ? ORDER BY name", ("table",)
        ).fetchall()
        print("Таблицы:", ", ".join(row[0] for row in tables) or "нет")
        exists = connection.execute(
            "SELECT 1 FROM sqlite_master WHERE type = ? AND name = ?", ("table", "tasks")
        ).fetchone()
        if exists:
            print("Задач:", connection.execute("SELECT COUNT(*) FROM tasks").fetchone()[0])
    finally:
        connection.close()


if __name__ == "__main__":
    main()
