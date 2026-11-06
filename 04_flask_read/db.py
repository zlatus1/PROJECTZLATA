
from __future__ import annotations

import logging
import sqlite3
from pathlib import Path

logger = logging.getLogger(__name__)
DEFAULT_DB_PATH = Path(__file__).resolve().parent / "app.db"


def get_connection(db_path: str | Path = DEFAULT_DB_PATH) -> sqlite3.Connection:
    connection = sqlite3.connect(str(db_path), timeout=5)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database(db_path: str | Path = DEFAULT_DB_PATH) -> None:
    connection = get_connection(db_path)
    try:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL CHECK(length(trim(title)) BETWEEN 1 AND 160),
                status TEXT NOT NULL DEFAULT 'new' CHECK(status IN ('new', 'done'))
            )
            """
        )
        connection.commit()
    except sqlite3.Error:
        connection.rollback()
        logger.exception("Database initialization failed")
        raise
    finally:
        connection.close()


def fetch_all_tasks(db_path: str | Path = DEFAULT_DB_PATH) -> list[sqlite3.Row]:
    connection = get_connection(db_path)
    try:
        cursor = connection.execute(
            "SELECT id, title, status FROM tasks "
            "ORDER BY CASE status WHEN 'new' THEN 0 ELSE 1 END, id DESC"
        )
        return cursor.fetchall()
    except sqlite3.Error:
        logger.exception("Could not read tasks")
        raise
    finally:
        connection.close()


def insert_task(title: str, db_path: str | Path = DEFAULT_DB_PATH) -> int:
    connection = get_connection(db_path)
    try:
        cursor = connection.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
        connection.commit()
        return int(cursor.lastrowid)
    except sqlite3.Error:
        connection.rollback()
        logger.exception("Could not add task")
        raise
    finally:
        connection.close()


def toggle_task_status(task_id: int, db_path: str | Path = DEFAULT_DB_PATH) -> int:
    connection = get_connection(db_path)
    try:
        cursor = connection.execute(
            """UPDATE tasks
               SET status = CASE WHEN status = 'done' THEN 'new' ELSE 'done' END
               WHERE id = ?""",
            (task_id,),
        )
        connection.commit()
        return cursor.rowcount
    except sqlite3.Error:
        connection.rollback()
        logger.exception("Could not update task")
        raise
    finally:
        connection.close()


def delete_task(task_id: int, db_path: str | Path = DEFAULT_DB_PATH) -> int:
    connection = get_connection(db_path)
    try:
        cursor = connection.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        connection.commit()
        return cursor.rowcount
    except sqlite3.Error:
        connection.rollback()
        logger.exception("Could not delete task")
        raise
    finally:
        connection.close()
