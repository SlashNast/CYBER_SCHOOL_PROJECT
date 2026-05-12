#users_db.py
import os
import sqlite3
from contextlib import closing
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

DB_PATH = os.path.join(os.path.dirname(__file__), "Users.db")

ph = PasswordHasher()

MATERIALS_DATA = [
    (1, "35571, H26", "pdf", r"C:\Users\Ulian\PycharmProjects\ciber2025\firstprojectcyber\pdfsBAGRUTMATH\horef2026 , שאלון-35571.pdf"),
    (2, "35571, H26, answers", "pdf", r"C:\Users\Ulian\PycharmProjects\ciber2025\firstprojectcyber\pdfsBAGRUTMATH\horef2026, פתרון,35571.pdf"),
    (3, "35572, H26", "pdf", r"C:\Users\Ulian\PycharmProjects\ciber2025\firstprojectcyber\pdfsBAGRUTMATH\שאלון-35572, horef2026.pdf"),
    (4, "35572, H26, answers", "pdf", r"C:\Users\Ulian\PycharmProjects\ciber2025\firstprojectcyber\pdfsBAGRUTMATH\horef2026, פתרון,35572.pdf"),
    (5, "35581, H26", "pdf", r"C:\Users\Ulian\PycharmProjects\ciber2025\firstprojectcyber\pdfsBAGRUTMATH\horef2026 , שאלון-35581.pdf"),
    (6, "35581, H26, answers", "pdf", r"C:\Users\Ulian\PycharmProjects\ciber2025\firstprojectcyber\pdfsBAGRUTMATH\horef2026, פתרון,35581.pdf"),
    (7, "35582, H26", "pdf", r"C:\Users\Ulian\PycharmProjects\ciber2025\firstprojectcyber\pdfsBAGRUTMATH\horef2026, שאלון- 35582.pdf"),
    (8, "35582, H26, answers", "pdf", r"C:\Users\Ulian\PycharmProjects\ciber2025\firstprojectcyber\pdfsBAGRUTMATH\horef2026, פתרון,35582.pdf"),
    (9, "35471, H26", "pdf", r"C:\Users\Ulian\PycharmProjects\ciber2025\firstprojectcyber\pdfsBAGRUTMATH\horef 2026, שאלון-35471.pdf"),
    (10, "35471, H26, answers", "pdf", r"C:\Users\Ulian\PycharmProjects\ciber2025\firstprojectcyber\pdfsBAGRUTMATH\horef2026, פתרון,35471.pdf"),
    (11, "35472, H26", "pdf", r"C:\Users\Ulian\PycharmProjects\ciber2025\firstprojectcyber\pdfsBAGRUTMATH\horef2026, שאלון,35472.pdf"),
    (12, "35472, H26, answers", "pdf", r"C:\Users\Ulian\PycharmProjects\ciber2025\firstprojectcyber\pdfsBAGRUTMATH\horef2026, פתרון,35472.pdf"),
    (13, "35481, H26", "pdf", r"C:\Users\Ulian\PycharmProjects\ciber2025\firstprojectcyber\pdfsBAGRUTMATH\horef2026, שאלון-35481.pdf"),
    (14, "35481, H26, answers", "pdf", r"C:\Users\Ulian\PycharmProjects\ciber2025\firstprojectcyber\pdfsBAGRUTMATH\horef2026, פתרון,35481.pdf"),
    (15, "35482, H26", "pdf", r"C:\Users\Ulian\PycharmProjects\ciber2025\firstprojectcyber\pdfsBAGRUTMATH\horef2026, שאלון-35482.pdf"),
    (16, "35482, H26, answers", "pdf", r"C:\Users\Ulian\PycharmProjects\ciber2025\firstprojectcyber\pdfsBAGRUTMATH\horef2026, פתרון,35482.pdf"),
    (17, "35371, H26", "pdf", r"C:\Users\Ulian\PycharmProjects\ciber2025\firstprojectcyber\pdfsBAGRUTMATH\horef2026, שאלון-35371.pdf"),
    (18, "35372, H26", "pdf", r"C:\Users\Ulian\PycharmProjects\ciber2025\firstprojectcyber\pdfsBAGRUTMATH\horef2026, שאלון-35372.pdf"),
    (19, "35372, H26, answers", "pdf", r"C:\Users\Ulian\PycharmProjects\ciber2025\firstprojectcyber\pdfsBAGRUTMATH\horef2026, פתרון,35372.pdf"),
    (20, "35381, H26", "pdf", r"C:\Users\Ulian\PycharmProjects\ciber2025\firstprojectcyber\pdfsBAGRUTMATH\horef2026, שאלון-35381.pdf"),
    (21, "35382, H26", "pdf", r"C:\Users\Ulian\PycharmProjects\ciber2025\firstprojectcyber\pdfsBAGRUTMATH\horef2026, שאלון-35382.pdf"),


    (22, "36282, S25", "pdf", r"C:\Users\Ulian\PycharmProjects\ciber2025\firstprojectcyber\pdfsBAGRUTPHYS\summer2025, שאלון,36282.pdf"),
    (23, "36282, S25, answers", "pdf", r"C:\Users\Ulian\PycharmProjects\ciber2025\firstprojectcyber\pdfsBAGRUTPHYS\summer2025, פתרון,36282.pdf"),
    (24, "36361, S25", "pdf", r"C:\Users\Ulian\PycharmProjects\ciber2025\firstprojectcyber\pdfsBAGRUTPHYS\summer2025, שאלון,36361.pdf"),
    (25, "36361, S25, answers", "pdf", r"C:\Users\Ulian\PycharmProjects\ciber2025\firstprojectcyber\pdfsBAGRUTPHYS\summer2025, פתרון,36361.pdf"),
    (26, "36371, S25", "pdf", r"C:\Users\Ulian\PycharmProjects\ciber2025\firstprojectcyber\pdfsBAGRUTPHYS\summer2025, שאלון,36371.pdf"),
    (27, "36371, S25, answers", "pdf", r"C:\Users\Ulian\PycharmProjects\ciber2025\firstprojectcyber\pdfsBAGRUTPHYS\summer2025, פתרון 36371.pdf"),
    (28, "36382, S25", "pdf", r"C:\Users\Ulian\PycharmProjects\ciber2025\firstprojectcyber\pdfsBAGRUTPHYS\summer2025, שאלון,36382.pdf"),
    (29, "36382, S25, answers", "pdf", r"C:\Users\Ulian\PycharmProjects\ciber2025\firstprojectcyber\pdfsBAGRUTPHYS\summer2025, פתרון,36382.pdf"),

    (30, "16381, S25", "pdf", r"C:\Users\Ulian\PycharmProjects\ciber2025\firstprojectcyber\pdfsBAGRUTENG\summer2025, שאלון-16381A.pdf"),
    (31, "16381, S25, answers", "pdf", r"C:\Users\Ulian\PycharmProjects\ciber2025\firstprojectcyber\pdfsBAGRUTENG\summer2025, פתרון-16381A.pdf"),
    (32, "16382, S25", "pdf", r"C:\Users\Ulian\PycharmProjects\ciber2025\firstprojectcyber\pdfsBAGRUTENG\summer2025, שאלון-16382C.pdf"),
    (33, "16382, S25, answers", "pdf", r"C:\Users\Ulian\PycharmProjects\ciber2025\firstprojectcyber\pdfsBAGRUTENG\summer2025, פתרון-16382C.pdf"),
    (34, "16582, S25", "pdf", r"C:\Users\Ulian\PycharmProjects\ciber2025\firstprojectcyber\pdfsBAGRUTENG\summer2025, שאלון-16582G.pdf"),
    (35, "16582, S25, answers", "pdf", r"C:\Users\Ulian\PycharmProjects\ciber2025\firstprojectcyber\pdfsBAGRUTENG\summer2025, פתרון-16581G.pdf"),
    (36, "16471, S25", "pdf", r"C:\Users\Ulian\PycharmProjects\ciber2025\firstprojectcyber\pdfsBAGRUTENG\summer2025, 16471-שאלוןE.pdf"),
    (37, "16471, S25, answers", "pdf", r"C:\Users\Ulian\PycharmProjects\ciber2025\firstprojectcyber\pdfsBAGRUTENG\summer2025, פתרון-16471E.pdf"),

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
            ON CONFLICT(id) DO UPDATE SET
            title = excluded.title,
            type = excluded.type,
            path_or_link = excluded.path_or_link
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



#---------- NOTES


def ensure_db_notes():
    with closing(sqlite3.connect(DB_PATH)) as con:
        con.execute("""
               CREATE TABLE IF NOT EXISTS Notes (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   user_id INTEGER NOT NULL,
                   title TEXT NOT NULL,  
                   content TEXT DEFAULT '',
                   created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                   updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                   FOREIGN KEY (user_id) REFERENCES Users(id)
               )
           """)
        con.commit()


def get_user_notes(user_id: int):
    with closing(sqlite3.connect(DB_PATH)) as con:
        cur = con.execute("""
            SELECT id, title, created_at
            FROM Notes
            WHERE user_id = ?
            ORDER BY updated_at DESC
        """, (user_id,))
        return cur.fetchall()


def get_note_by_id(note_id: int, user_id: int):
    ensure_db_notes()

    with closing(sqlite3.connect(DB_PATH)) as con:
        row = con.execute("""
            SELECT id, title, content, created_at, updated_at
            FROM Notes
            WHERE id = ? AND user_id = ?
        """, (note_id, user_id)).fetchone()

    return row



def add_note(user_id: int, title: str, content: str = ""):
    ensure_db_notes()

    with closing(sqlite3.connect(DB_PATH)) as con:
        cur = con.execute("""
            INSERT INTO Notes (user_id, title, content)
            VALUES (?, ?, ?)
        """, (user_id, title, content))
        con.commit()
        return cur.lastrowid



def update_note(note_id: int, user_id: int, title: str, content: str):
    with closing(sqlite3.connect(DB_PATH)) as con:
        con.execute("""
            UPDATE Notes
            SET title = ?, content = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ? AND user_id = ?
        """, (title, content, note_id, user_id))
        con.commit()


def delete_note(note_id: int, user_id: int):
    with closing(sqlite3.connect(DB_PATH)) as con:
        cur = con.execute("""
            DELETE FROM Notes
            WHERE id = ? AND user_id = ?
        """, (note_id, user_id))
        con.commit()
        return cur.rowcount > 0







