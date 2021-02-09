# Display107a.py
# Blinker, constructor with parameters

from py7seg import Py7Seg

ps = Py7Seg()
text = "boot"
ps.showBlinker(text, dp = [0, 0, 0, 1], count = 4, speed = 2, blocking = True)
ps.showText("8ye")
