# Display101.py
# showText()

from py7seg import Py7Seg
import time

ps = Py7Seg()
print "showText('1234')"
ps.showText('1234')
time.sleep(3)
print "showText('1234567890')"
ps.showText('1234567890')
time.sleep(3)
print "showText('1234567890' pos = 2)"
ps.showText('1234567890', pos = 2)
time.sleep(3)
print "showText('1234567890', pos = -2)"
ps.showText('1234567890', pos = -2)
time.sleep(3)
print "showText('1234567890', pos = 1, dp = [1, 1, 0])"
ps.showText('1234567890', pos = 1, dp = [1, 1, 0])
time.sleep(3)
print "showText('1234567890', pos = 1, dp = [0, 1])"
ps.showText('1234567890', pos = 1, dp = [0, 1])
time.sleep(3)
print "All done"
