import sqlite3

# 1️⃣ Connexion à la base de données (ou création si elle n'existe pas)
conn = sqlite3.connect("ma_base.db")  # fichier ma_base.db
cursor = conn.cursor()

# 2️⃣ Création d'une table
cursor.execute("""
CREATE TABLE IF NOT EXISTS utilisateurs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
)
""")

# 3️⃣ Insertion de données
utilisateurs = [
    ("Alice", "alice@example.com"),
    ("Bob", "bob@example.com"),
    ("Charlie", "charlie@example.com")
]

cursor.executemany("INSERT INTO utilisateurs (nom, email) VALUES (?, ?)", utilisateurs)

# 4️⃣ Sauvegarde (commit) des modifications
conn.commit()

# 5️⃣ Lecture des données
cursor.execute("SELECT * FROM utilisateurs")
rows = cursor.fetchall()
for row in rows:
    print(row)

# 6️⃣ Fermeture de la connexion
conn.close()
