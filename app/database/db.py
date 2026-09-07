import sqlite3
from pathlib import Path
from typing import Any, Optional

from app.config.settings import DB_PATH


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def ensure_parent_dir() -> None:
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)


def mark_update_processed(update_id: str) -> None:
    ensure_parent_dir()
    with get_connection() as conn:
        conn.execute(
            "INSERT OR IGNORE INTO idempotency (update_id, processed_at) VALUES (?, datetime('now'))",
            (update_id,),
        )


def was_update_processed(update_id: str) -> bool:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT 1 FROM idempotency WHERE update_id = ?",
            (update_id,),
        ).fetchone()
        return row is not None


def db_exists() -> bool:
    return Path(DB_PATH).exists()
