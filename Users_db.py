import os
import sqlite3
from contextlib import closing
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

DB_PATH = os.path.join(os.path.dirname(__file__), "Users.db")
ph = PasswordHasher()

def ensure_db() -> None:
    with closing(sqlite3.connect(DB_PATH)) as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS Users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                login TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        con.commit()

def add_user(login: str, password: str) -> bool:
    ensure_db()
    login = (login or "").strip()
    password = (password or "").strip()
    if not login or not password:
        return False

    pw_hash = ph.hash(password)

    with closing(sqlite3.connect(DB_PATH)) as con:
        try:
            con.execute(
                "INSERT INTO Users (login, password_hash) VALUES (?, ?)",
                (login, pw_hash)
            )
            con.commit()
            return True
        except sqlite3.IntegrityError:
            return False

def check_user(login: str, password: str) -> bool:
    ensure_db()
    login = (login or "").strip()
    password = (password or "").strip()
    if not login or not password:
        return False

    with closing(sqlite3.connect(DB_PATH)) as con:
        row = con.execute(
            "SELECT password_hash FROM Users WHERE login = ?",
            (login,)
        ).fetchone()

    if not row:
        return False

    try:
        return ph.verify(row[0], password)
    except VerifyMismatchError:
        return False