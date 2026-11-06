
import argparse

from db import DEFAULT_DB_PATH, get_connection, initialize_database


def main() -> None:
    parser = argparse.ArgumentParser(description="Create the task manager database.")
    parser.add_argument("--seed", action="store_true", help="add a few clearly marked sample tasks")
    parser.add_argument("--db", default=str(DEFAULT_DB_PATH), help="database file path")
    args = parser.parse_args()

    initialize_database(args.db)
    if args.seed:
        connection = get_connection(args.db)
        try:
            count = connection.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
            if count == 0:
                connection.executemany(
                    "INSERT INTO tasks (title, status) VALUES (?, ?)",
                    [("Пример: проверить список задач", "new"), ("Пример: изучить SQLite", "done")],
                )
                connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()
    print(f"База готова: {args.db}")


if __name__ == "__main__":
    main()
