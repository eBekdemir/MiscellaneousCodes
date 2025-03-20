__author__ = "Kömen - Enes Bekdemir | 2024"
"""
    This is a simple Morse code generator using the ESP8266 board.
"""

from machine import Pin
from time import sleep

led = Pin(5, Pin.OUT)

mors = {
    'a': [0, 1],
    'b': [1, 0, 0, 0],
    'c': [1, 0, 1, 0],
    'd': [1, 0, 0],
    'e': [0],
    'f': [0, 0, 1, 0],
    'g': [1, 1, 0],
    'h': [0, 0, 0, 0],
    'i': [0, 0],
    'j': [0, 1, 1, 1],
    'k': [1, 0, 1],
    'l': [0, 1, 0, 0],
    'm': [1, 1],
    'n': [1, 0],
    'o': [1, 1, 1],
    'p': [0, 1, 1, 0],
    'q': [1, 1, 0, 1],
    'r': [0, 1, 0],
    
    's': [0, 0, 0],
    't': [1],
    'u': [0, 0, 1],
    'v': [0, 0, 0, 1],
    'w': [0, 1, 1],
    'x': [1, 0, 0, 1],
    'y': [1, 0, 1, 1],
    'z': [1, 1, 0, 0],
    ' ': []
}

def show(lett, led=led):
    for proc in mors[lett]:
        if proc:
            led.on()
            sleep(0.7)
            led.off()
        else:
            led.on()
            sleep(0.3)
            led.off()
        sleep(0.3)


led.off()
while True:
    text = input('Text:: ').strip().lower()
    if text == 'exit': break
    for letter in text:
        if letter in mors:
            show(letter, led)
            sleep(1)
        if letter == ' ':
            sleep(1.5) 
