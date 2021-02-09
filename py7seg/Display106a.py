# Display106a.py
# Ticker, constructor with parameters

from py7seg import Py7Seg

ps = Py7Seg()
ip = "x192-168-1-13"
ps.showTicker(ip, count = 2, speed = 4, blocking = True)
ps.showText("donE")
