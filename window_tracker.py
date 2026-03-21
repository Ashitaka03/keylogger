# ============================================================
#  window_tracker.py — Récupère le nom de la fenêtre active
#  Rôle : savoir dans quel logiciel chaque frappe est tapée
#  Dépendances : pygetwindow (Windows) ou xdotool (Linux)
#
#  Sans ce module, tous les logs affichent window="unknown"
#  Avec ce module : window="Chrome", "VSCode", "Terminal"...
# ============================================================

# ── CONCEPT : LA FENÊTRE ACTIVE ──────────────────────────────
# À chaque instant, le système d'exploitation sait quelle fenêtre
# a le "focus" — c'est celle qui reçoit les frappes clavier.
# On interroge l'OS pour récupérer son titre.
#
# Le problème : chaque OS expose cette info différemment
#   Windows → module pygetwindow (pip install pygetwindow)
#   Linux   → commande système xdotool (apt install xdotool)
#   macOS   → module AppKit (natif sur mac)
#
# Solution : on détecte l'OS au runtime et on appelle
# la bonne méthode — c'est ce qu'on appelle de l'abstraction

import sys
import subprocess


def get_active_window():
    """
    Retourne le titre de la fenêtre active selon l'OS.

    Retourne :
        str — titre de la fenêtre  ex: "index.html - VSCode""unknown" si la récupération échoue
    """

    # sys.platform retourne :
    #   "win32"  → Windows (même sur 64 bits)
    #   "linux"  → Linux
    #   "darwin" → macOS

    if sys.platform == "win32":
        return _get_window_windows()

    elif sys.platform == "linux":
        return _get_window_linux()

    elif sys.platform == "darwin":
        return _get_window_mac()

    else:
        return "unknown"


# ── IMPLÉMENTATION WINDOWS ───────────────────────────────────

def _get_window_windows():
    """
    Utilise pygetwindow pour récupérer la fenêtre active.
    Installation : pip install pygetwindow
    """
    try:
        import pygetwindow as gw
        # getActiveWindow() retourne l'objet fenêtre active
        # .title est son titre (barre de titre de la fenêtre)
        window = gw.getActiveWindow()
        if window:
            return window.title or "unknown"
        return "unknown"

    except ImportError:
        # pygetwindow pas installé → on guide l'utilisateur
        print("[window_tracker] pip install pygetwindow")
        return "unknown"

    except Exception:
        return "unknown"


# ── IMPLÉMENTATION LINUX ─────────────────────────────────────

def _get_window_linux():
    """
    Utilise la commande système xdotool.
    Installation : sudo apt install xdotool

    subprocess.check_output() exécute une commande shell
    et retourne son output sous forme de bytes.
    """
    try:
        # xdotool getactivewindow  → retourne l'ID de la fenêtre
        # xdotool getwindowname ID → retourne son titre
        # On chaîne les deux avec $(...)
        result = subprocess.check_output(
            ["xdotool", "getactivewindow", "getwindowname"],
            stderr=subprocess.DEVNULL  # on ignore les erreurs dans le terminal
        )
        # decode("utf-8") convertit bytes → str
        # .strip() supprime le \n final
        return result.decode("utf-8").strip() or "unknown"

    except FileNotFoundError:
        # xdotool pas installé
        print("[window_tracker] sudo apt install xdotool")
        return "unknown"

    except Exception:
        return "unknown"


# ── IMPLÉMENTATION MACOS ─────────────────────────────────────

def _get_window_mac():
    """
    Utilise AppKit — natif sur macOS, pas d'installation nécessaire.
    NSWorkspace donne accès aux infos sur les apps en cours.
    """
    try:
        from AppKit import NSWorkspace
        # frontmostApplication() = l'app au premier plan
        # .localizedName = son nom lisible
        app = NSWorkspace.sharedWorkspace().frontmostApplication()
        return app.localizedName() or "unknown"

    except ImportError:
        return "unknown"

    except Exception:
        return "unknown"


# ── TEST STANDALONE ──────────────────────────────────────────
if __name__ == "__main__":
    print(f"OS détecté : {sys.platform}")
    print(f"Fenêtre active : {get_active_window()}")
    print("\nTest en continu (Ctrl+C pour arrêter) :")

    import time
    last = ""
    while True:
        current = get_active_window()
        # On affiche uniquement quand la fenêtre change
        if current != last:
            print(f"  → {current}")
            last = current
        time.sleep(0.5)