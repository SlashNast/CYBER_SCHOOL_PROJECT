# import json
#
# REG_LOGIN_CMD = ("REG", "SIGNIN")
#
# def create_response_msg_DB(cmd: str, args: list) -> str:
#     try:
#         if not args:
#             return json.dumps({"success": False, "error": "Missing args"})
#
#         data = json.loads(args[0])
#         login = (data.get("login") or "").strip()
#         password = (data.get("password") or "").strip()
#
#         if cmd == "REG":
#             if not login or not password:
#                 return json.dumps({"success": False, "error": "Empty login/password"})
#             return json.dumps({"success": True, "msg": f"User {login} registered"})
#
#         if cmd == "SIGNIN":
#             if not login or not password:
#                 return json.dumps({"success": False, "error": "Empty login/password"})
#             return json.dumps({"success": True, "msg": f"Welcome {login}"})
#
#         return json.dumps({"success": False, "error": "Unknown DB cmd"})
#     except Exception as e:
#         return json.dumps({"success": False, "error": str(e)})


import json
import sqlite3
from datetime import datetime

DB_NAME = "Users.db"
TABLE_USERS = "Users"

REG_LOGIN_CMD = ("REG", "SIGNIN")


def _get_conn():
    return sqlite3.connect(DB_NAME, check_same_thread=False)


def _ensure_tables():
    conn = _get_conn()
    try:
        cur = conn.cursor()
        # cur.execute(f"""
        #     CREATE TABLE IF NOT EXISTS {TABLE_USERS} (
        #         id INTEGER PRIMARY KEY AUTOINCREMENT,
        #         login TEXT UNIQUE NOT NULL,
        #         password TEXT NOT NULL,
        #         created_at TEXT NOT NULL
        #     )
        # """)
        #
        #

        cur.execute(f"""
                   CREATE TABLE IF NOT EXISTS {TABLE_USERS} (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       login TEXT UNIQUE NOT NULL
                   )
               """)

        conn.commit()

        cur.execute(f"PRAGMA table_info({TABLE_USERS})")
        cols = {row[1] for row in cur.fetchall()}  # row[1] = column name

        if "password" not in cols:
            cur.execute(f"ALTER TABLE {TABLE_USERS} ADD COLUMN password TEXT")
        if "created_at" not in cols:
            cur.execute(f"ALTER TABLE {TABLE_USERS} ADD COLUMN created_at TEXT")

        conn.commit()

    finally:
        conn.close()


def _user_exists(cur, login: str) -> bool:
    cur.execute(f"SELECT 1 FROM {TABLE_USERS} WHERE login = ?", (login,))
    return cur.fetchone() is not None


def _check_password(cur, login: str, password: str) -> bool:
    cur.execute(f"SELECT password FROM {TABLE_USERS} WHERE login = ?", (login,))
    row = cur.fetchone()
    if row is None:
        return False
    return row[0] == password


def create_response_msg_DB(cmd: str, args: list) -> str:
    """
    args[0] должен быть JSON-строкой: {"login":"...", "password":"..."}
    Возвращает JSON-строку (payload), БЕЗ length-prefix.
    """
    try:
        _ensure_tables()

        if not args:
            return json.dumps({"success": False, "error": "Missing args"})

        # ВАЖНО: из-за твоего get_cmd_and_args args приходит как list,
        # и JSON лежит в args[0]
        data = json.loads(args[0])

        login = (data.get("login") or "").strip()
        password = (data.get("password") or "").strip()

        if not login or not password:
            return json.dumps({"success": False, "error": "Empty login/password"})

        conn = _get_conn()
        try:
            cur = conn.cursor()

            if cmd == "REG":
                if _user_exists(cur, login):
                    return json.dumps({"success": False, "error": "User already exists"})

                cur.execute(
                    f"INSERT INTO {TABLE_USERS} (login, password, created_at) VALUES (?, ?, ?)",
                    (login, password, datetime.now().isoformat(timespec="seconds"))
                )
                conn.commit()
                return json.dumps({"success": True, "msg": f"User {login} registered"})

            if cmd == "SIGNIN":
                if not _user_exists(cur, login):
                    return json.dumps({"success": False, "error": "User not found"})

                if not _check_password(cur, login, password):
                    return json.dumps({"success": False, "error": "Wrong password"})

                return json.dumps({"success": True, "msg": f"Welcome {login}"})

            return json.dumps({"success": False, "error": "Unknown DB cmd"})
        finally:
            conn.close()

    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})

