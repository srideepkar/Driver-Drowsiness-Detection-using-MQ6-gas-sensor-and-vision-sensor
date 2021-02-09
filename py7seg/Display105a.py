# Display105a.py
# Display announcement

from py7seg import Py7Seg
import time

ps = Py7Seg()
text = "Py7Seg DISPLAY"
ps.showText(text)
k = 0
while True:
    time.sleep(0.5)
    nb = ps.scrollToLeft()
    if nb == 0:
        if k == 1:
            break
        ps.setToStart()
        k += 1
ps.showText("donE")
