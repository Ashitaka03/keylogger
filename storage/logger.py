import sqlite3

con = sqlite3.connect('keylogs.db')
cur = con.cursor()
#___________________________________________________________creation de la table_____________________________________________
def create_table():
    cur.execute(""" CREATE TABLE IF NOT EXISTS keylogs(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    key TEXT,
    window TEXT,
    session_id TEXT)
    """)
    con.commit()

#___________________________________________________________ insertion de données____________________________________________

def insert_data(timestamp, key, window, session_id):
    timestamp = input("Enter timestamp (YYYY-MM-DD HH:MM:SS): ")
    key = input("Enter key: ")
    window = input("Enter window: ")                 #input temporaire a remplacer pars variable
    session_id = input("Enter session_id: ")
    cur.execute("INSERT INTO keylogs(timestamp, key, window, session_id) VALUES (?, ?, ?, ?)", (timestamp, key, window, session_id))
    con.commit()
#____________________________________________________________affichage de toutes les données____________________________________________
def find_by_timestamp(timestamp1, timestamp2):#chercher par timestamp
    cur.execute("SELECT timestamp FROM keylogs WHERE timestamp BETWEEN ? AND ? ORDER BY timestamp", (timestamp1, timestamp2))
    raw1 = cur.fetchall()
    print(raw1)

def find_by_key(key):#chercher par key
    cur.execute("SELECT * FROM keylogs WHERE key = ? ORDER BY key", (key,))
    raw2 = cur.fetchall()
    print(raw2)

def find_by_window(window):#chercher par window
    cur.execute("SELECT * FROM keylogs WHERE window = ? ORDER BY window", (window,))
    raw3 = cur.fetchall()
    print(raw3)

def find_by_session_id(session_id):#chercher par session_id
    cur.execute("SELECT * FROM keylogs WHERE session_id = ? ORDER BY session_id", (session_id,))
    raw4 = cur.fetchall()
    print(raw4)

#____________________________________________________________execution du code____________________________________________
create_table()
insert_data("2023-10-10 12:00:00", "a", "Window1", "Session1")