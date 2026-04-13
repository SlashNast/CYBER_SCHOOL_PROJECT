#users_db.py
import os
import sqlite3
from contextlib import closing
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

DB_PATH = os.path.join(os.path.dirname(__file__), "Users.db")

ph = PasswordHasher()

MATERIALS_DATA = [
    (1, "35571, H26", "pdf", r"C:\Users\Ulian\PycharmProjects\ciber2025\firstprojectcyber\pdfsBAGRUTMATH\שאלון-35571,  horef2026 .pdf"),
    (2, "35572, H26", "pdf", r"C:\Users\Ulian\PycharmProjects\ciber2025\firstprojectcyber\pdfsBAGRUTMATH\שאלון-35572, horef2026.pdf"),
    (3, "35581, H26", "pdf", r"C:\Users\Ulian\PycharmProjects\ciber2025\firstprojectcyber\pdfsBAGRUTMATH\horef2026 , שאלון-35581.pdf"),
    (4, "35582, H26", "pdf", r"C:\Users\Ulian\PycharmProjects\ciber2025\firstprojectcyber\pdfsBAGRUTMATH\horef2026, שאלון- 35582.pdf"),
    (5, "35471, H26", "pdf", r"C:\Users\Ulian\PycharmProjects\ciber2025\firstprojectcyber\pdfsBAGRUTMATH\horef 2026, שאלון-35471.pdf"),
    (6, "35472, H26", "pdf", r"C:\Users\Ulian\PycharmProjects\ciber2025\firstprojectcyber\pdfsBAGRUTMATH\horef2026, שאלון,35472.pdf"),
    (7, "35481, H26", "pdf", r"C:\Users\Ulian\PycharmProjects\ciber2025\firstprojectcyber\pdfsBAGRUTMATH\horef2026, שאלון-35481.pdf"),
    (8, "35482, H26", "pdf", r"C:\Users\Ulian\PycharmProjects\ciber2025\firstprojectcyber\pdfsBAGRUTMATH\horef2026, שאלון-35482.pdf"),
    (9, "35371, H26", "pdf", r"C:\Users\Ulian\PycharmProjects\ciber2025\firstprojectcyber\pdfsBAGRUTMATH\horef2026, שאלון-35371.pdf"),
    (10, "35372, H26", "pdf", r"C:\Users\Ulian\PycharmProjects\ciber2025\firstprojectcyber\pdfsBAGRUTMATH\horef2026, שאלון-35372.pdf"),
    (11, "35381, H26", "pdf", r"C:\Users\Ulian\PycharmProjects\ciber2025\firstprojectcyber\pdfsBAGRUTMATH\horef2026, שאלון-35381.pdf"),
    (12, "35382, H26", "pdf", r"C:\Users\Ulian\PycharmProjects\ciber2025\firstprojectcyber\pdfsBAGRUTMATH\horef2026, שאלון-35382.pdf"),
    (13, "1 task video", "link", "https://youtu.be/0XczPenRWOk"),
    (14, "2 task video", "link","https://youtu.be/qca6bfIqrFk"),
    (15, "3 task video", "link", "https://youtu.be/jdb4Btc9lDw"),
    (16, "4 task video", "link", "https://youtu.be/pS_6_b_o-I4"),
    (17, "5 task video", "link", "https://youtu.be/xwVU5mzXNSE"),
    (18, "6 task video", "link",  "https://youtu.be/hIYzABmh6IU"),
    (19, "7 task video", "link", "https://youtu.be/OjfGz1ydfPQ"),
    (20, "8 task video", "link", "https://youtu.be/-k3BcZaUMm0"),
    (21, "36282, S25", "pdf", r"C:\Users\Ulian\PycharmProjects\ciber2025\firstprojectcyber\pdfsBAGRUTPHYS\summer2025, שאלון,36282.pdf"),
    (22, "35361, S25", "pdf", r"C:\Users\Ulian\PycharmProjects\ciber2025\firstprojectcyber\pdfsBAGRUTPHYS\summer2025, שאלון,36361.pdf"),
    (23, "35371, S25", "pdf", r"C:\Users\Ulian\PycharmProjects\ciber2025\firstprojectcyber\pdfsBAGRUTPHYS\summer2025, שאלון,36371.pdf"),
    (24, "35382, S25", "pdf", r"C:\Users\Ulian\PycharmProjects\ciber2025\firstprojectcyber\pdfsBAGRUTPHYS\summer2025, שאלון,36382.pdf"),

]



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



def get_user_id(login: str) -> int | None:
    ensure_db()
    login = (login or "").strip()

    with closing(sqlite3.connect(DB_PATH)) as con:
        row = con.execute(
            "SELECT id FROM Users WHERE login = ?",
            (login,)
        ).fetchone()

    if row:
        return row[0]
    return None



#---------- TABLE MATERIALS

def seed_materials() -> None:
    ensure_db_materials()

    with closing(sqlite3.connect(DB_PATH)) as con:
        con.executemany("""
            INSERT OR IGNORE INTO Materials (id, title, type, path_or_link)
            VALUES (?, ?, ?, ?)
        """, MATERIALS_DATA)
        con.commit()




def ensure_db_materials() -> None:
    with closing(sqlite3.connect(DB_PATH)) as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS Materials (
                id INTEGER PRIMARY KEY ,
                title TEXT NOT NULL UNIQUE,
                type TEXT NOT NULL,
                path_or_link TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        con.commit()



#---------- USER FAVORITES

def ensure_db_favorites() -> None:
    with closing(sqlite3.connect(DB_PATH)) as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS Favorites (
                user_id INTEGER NOT NULL,
                material_id INTEGER NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (user_id, material_id),
                FOREIGN KEY (user_id) REFERENCES Users(id),
                FOREIGN KEY (material_id) REFERENCES Materials(id)
            )
        """)
        con.commit()

def add_to_favorites(user_id: int, material_id: int) -> bool:
    ensure_db()
    ensure_db_materials()
    ensure_db_favorites()

    if not user_id or not material_id:
        return False

    try:
        with closing(sqlite3.connect(DB_PATH)) as con,con:
            con.execute("""
                            INSERT INTO Favorites (user_id, material_id)
                            VALUES (?, ?)
                        """, (user_id, material_id))
        return True
    except sqlite3.IntegrityError:
        return False



def remove_from_favorites(user_id: int, material_id: int) -> bool:
    with closing(sqlite3.connect(DB_PATH)) as con, con:
        cur = con.execute("""
            DELETE FROM Favorites
            WHERE user_id = ? AND material_id = ?
        """, (user_id, material_id))
        return cur.rowcount > 0


def get_user_favorite_materials(user_id: int):
    with closing(sqlite3.connect(DB_PATH)) as con:
        rows = con.execute("""
            SELECT Materials.id, Materials.title,  Materials.path_or_link
            FROM Favorites
            JOIN Materials ON Favorites.material_id = Materials.id
            WHERE Favorites.user_id = ?
            ORDER BY Favorites.created_at DESC
        """, (user_id,)).fetchall()

    return rows



def get_material_id_by_title(title: str) -> int | None:
    ensure_db_materials()

    with closing(sqlite3.connect(DB_PATH)) as con:
        row = con.execute(
            "SELECT id FROM Materials WHERE title = ?",
            (title,)
        ).fetchone()

    if row:
        return row[0]
    return None




