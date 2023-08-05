from keyboard import write, press
from time import sleep

keybind = "enter"
text = "pySpam default text"

def wait(t):
	sleep( int(t) )

def send(msg = text, key = keybind, times = 1):
	for x in range(times):
		write( str ( txt ) )
		wait(0.07)
		press( str(key) )

def change_keybind(key):
	keybind == str(key)

def change_text(txt):
	text == str(txt)
