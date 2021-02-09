# Display105.py
# Scroll setToStart()

from py7seg import Py7Seg
import time

ps = Py7Seg()
time.sleep(3)

print "showText('1234567890', pos = 2)"
ps.showText('1234567890', 2)
time.sleep(3)
k = 0
while True:
    print "scrollToLeft()"
    nb = ps.scrollToLeft()
    print "remaining:", nb
    time.sleep(3)
    if nb == 0:
        print "setToStart()"
        ps.setToStart()
        time.sleep(3)
        k += 1
        if k == 2:
            break
ps.showText("donE")
