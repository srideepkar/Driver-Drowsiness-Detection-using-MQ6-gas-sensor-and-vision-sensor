# Display107.py
# Blinker, default constructor

from py7seg import Py7Seg

ps = Py7Seg()
text = "boot"
ps.showBlinker(text)
while ps.isBlinkerAlive():
    continue
ps.showText("8ye")
