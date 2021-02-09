# Display104.py
# Scroll text to right

from py7seg import Py7Seg
import time

ps = Py7Seg()

print "showText('1234567890', pos = 2)"
rc = ps.showText('1234567890', pos = 2)
time.sleep(3)
for i in range(6):
    print "scrollToRight()"
    nb = ps.scrollToRight()
    print "remaining:", nb
    time.sleep(3)
ps.showText("donE")
