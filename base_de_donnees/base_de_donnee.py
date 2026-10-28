import sqlite3
import threading
import os

db_shutdown = threading.Event()

# -- chemin absolu pour éviter le problème de fichier "perdu"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "donnees.db")

# Connexion SQLite thread-safe
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
conn.row_factory = sqlite3.Row
curs = conn.cursor()

# Créer la table si elle n'existe pas
curs.execute("""
CREATE TABLE IF NOT EXISTS donnees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    donnee TEXT NOT NULL
)
""")
conn.commit()

# Verrou global pour protéger le curseur et la connexion
db_lock = threading.Lock()

# -- Fonctions CRUD robustes --


def selection():
    if db_shutdown.is_set():
        raise RuntimeError("Database is shutting down")
    with db_lock:
        curs.execute("SELECT * FROM donnees")
        rows = curs.fetchall()
    # Retourne une liste de dictionnaires pour FastAPI
    return [{"id": r[0], "donnee": r[1]} for r in rows]


def creation(donnee_add):
    if db_shutdown.is_set():
        raise RuntimeError("Database is shutting down")
    with db_lock:
        curs.execute("INSERT INTO donnees (donnee) VALUES (?)", (donnee_add,))
        conn.commit()


def modification(id_donnee, nouvelle_donnee):
    if db_shutdown.is_set():
        raise RuntimeError("Database is shutting down")
    with db_lock:
        curs.execute(
            "UPDATE donnees SET donnee = ? WHERE id = ?", (nouvelle_donnee, id_donnee)
        )
        conn.commit()


def deletion(id_donnee):
    if db_shutdown.is_set():
        raise RuntimeError("Database is shutting down")
    with db_lock:
        curs.execute("DELETE FROM donnees WHERE id = ?", (id_donnee,))
        conn.commit()


def test():
    try:
        curs.execute("PRAGMA database_list")
        db = curs.fetchall()
        print("BASE SQLITE :", db)

        curs.execute("""
                     SELECT name
                     FROM sqlite_master
                     WHERE type = 'table'
                     """)
        tables = curs.fetchall()
        print("TABLES :", tables)

        curs.execute("SELECT description FROM donnees")
        data = curs.fetchall()

        return {"data": data}

    except Exception as e:
        print("ERREUR :", e)
        return {"error": str(e)}


def stopdb():
    db_shutdown.set()
    with db_lock:
        try:
            curs.close()
            conn.close()
        except Exception as e:
            print(f"Erreur fermeture SQLite : {e}")
