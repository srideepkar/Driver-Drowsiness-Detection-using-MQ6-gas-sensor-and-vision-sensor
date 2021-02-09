# Display101.py
# showText()

from py7seg import Py7Seg
import time

ps = Py7Seg()
ps.showText('HELO')
for i in range(4):
    time.sleep(0.5)
    ps.setBrightness(7)
    time.sleep(0.5)
    ps.setBrightness(1)
time.sleep(1)
ps.showText("8YE")
