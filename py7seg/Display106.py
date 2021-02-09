# Display106.py
# Ticker, default constructor

from py7seg import Py7Seg

ps = Py7Seg()
ip = "x192-168-1-13"
ps.showTicker(ip)
while ps.isTickerAlive():
    continue
ps.showText("donE")
