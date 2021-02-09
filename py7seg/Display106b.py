# Display106b.py
# Ticker, infinite duration

from py7seg import Py7Seg
import time

ps = Py7Seg()
ip = "x192-168-1-13"
ps.showTicker(ip, count = 0)
print "Sleeping now..."
time.sleep(10)
print "Waking up..."
ps.stopTicker()
time.sleep(3)
ps.showText("donE")
