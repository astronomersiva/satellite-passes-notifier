import pynotify
from datetime import datetime

thisDateTime = datetime.now()
thisYear = thisDateTime.year
thisMonth = thisDateTime.strftime("%b")
thisDay = thisDateTime.day
thisHour = thisDateTime.hour
thisMin = thisDateTime.strftime("%M")
print thisDay, thisHour, thisMin
pynotify.init("iss")
with open('IridiumNotifier.txt', 'r') as inputFile:
    passes = inputFile.read().splitlines()
    for irPass in passes:
       passDate, passHour, passMin, passMag, where2See = irPass.split('|')
       if int(passDate) == int(thisDay) and int(thisHour) == int(passHour):
           n = pynotify.Notification("Iridium Flare",
                "At " + str(passHour) + ": " + str(passMin) + '\n' + "Intensity: " + passMag + '\n' + where2See
                )
           n.show()
