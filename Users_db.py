# Users_db.py
import os, sqlite3
from contextlib import closing

DB_PATH = os.path.join(os.path.dirname(__file__), "Users.db")

def ensure_db():
    with closing(sqlite3.connect(DB_PATH)) as con, con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS Users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                login TEXT NOT NULL UNIQUE,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

def add_user(login: str):
    ensure_db()
    login = (login or "").strip()
    if not login:
        print("SKIP empty login")
        return
    with closing(sqlite3.connect(DB_PATH)) as con:
        cur = con.execute("SELECT COUNT(*) FROM Users WHERE login = ?", (login,))
        cnt = cur.fetchone()[0]
        print("BEFORE:", os.path.abspath(DB_PATH), "| login =", repr(login), "| exists =", cnt)

        try:
            con.execute("INSERT INTO Users(login) VALUES (?)", (login,))
            con.commit()
            print("INSERTED OK")
        except sqlite3.IntegrityError as e:
            print("INTEGRITY ERROR:", e)  # <- увидим точную причину
            # con.execute("INSERT OR IGNORE INTO Users(login) VALUES (?)", (login,))
            # con.commit()
