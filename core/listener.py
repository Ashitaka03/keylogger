from pynput import keyboard

def action_clavier(key):
    try:
        if key.char == 'q':
            print("teste ")
            return False  # 
    except AttributeError:
        pass  

    print("teste 2")

with keyboard.Listener(on_press=action_clavier) as listener:
    listener.join()

