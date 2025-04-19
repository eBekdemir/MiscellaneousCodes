import keyboard
import sys
def text_to_binary(text):
    return ' '.join(format(byte, '08b') for byte in text.encode())

def on_key_event(e):
    if e.event_type == 'down':
        if e.name == 'esc':
            print("Exiting...")
            sys.exit(0)
        elif e.name == 'space':
            keyboard.press_and_release('backspace')
            keyboard.write(text_to_binary(' ') + ' ')
        elif e.name == 'enter': pass
        elif len(e.name) > 1: pass
        else:
            keyboard.press_and_release('backspace')
            keyboard.write(text_to_binary(e.name) + ' ')
keyboard.hook(on_key_event)
keyboard.wait('esc')
