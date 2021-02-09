# Display102.py
# Show displayable chars
# Enter text from terminal

from py7seg import Py7Seg

print "Displayable chars:", Py7Seg.getDisplayableChars()
ps = Py7Seg()
ps.showText("run")
while True:
    print "Enter text (x to terminate)",
    text = raw_input() # Fetch the input from the terminal
    if text == "x":
        break
    ps.showText(text)
ps.showText("donE")
