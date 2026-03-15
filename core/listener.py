from pynput import keyboard

import threading #arrier plan

from datetime import datetime #horaire chaque frape

import os

################# HOOKS SYSTEME ########
def action_clavier(key):
    try:
        if key.char == 'q':
            print("teste")
            return False
        print("teste 2")
    except AttributeError:
        pass

with keyboard.Listener(on_press=action_clavier) as listener:
    listener.join()

