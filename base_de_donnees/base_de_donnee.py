import sqlite3
import threading
import os

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
    donnee TEXT
)
""")
conn.commit()

# Verrou global pour protéger le curseur et la connexion
db_lock = threading.Lock()

# -- Fonctions CRUD robustes --


def selection():
    with db_lock:
        curs.execute("SELECT * FROM donnees")
        rows = curs.fetchall()
    # Retourne une liste de dictionnaires pour FastAPI
    return [{"id": r[0], "donnee": r[1]} for r in rows]


def creation(donnee_add):
    with db_lock:
        curs.execute("INSERT INTO donnees (donnee) VALUES (?)", (donnee_add,))
        conn.commit()


def modification(id_donnee, nouvelle_donnee):
    with db_lock:
        curs.execute(
            "UPDATE donnees SET donnee = ? WHERE id = ?", (nouvelle_donnee, id_donnee)
        )
        conn.commit()


def deletion(id_donnee):
    with db_lock:
        curs.execute("DELETE FROM donnees WHERE id = ?", (id_donnee,))
        conn.commit()
