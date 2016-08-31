#This Python file uses the following encoding: utf-8
#import pynotify
from platform import system
from pync import Notifier
from datetime import datetime

thisDateTime = datetime.now()
thisYear = thisDateTime.year
thisMonth = thisDateTime.strftime("%b")
thisDay = thisDateTime.day
thisHour = thisDateTime.hour
thisMin = thisDateTime.strftime("%M")

#pynotify.init("iridium")

with open('IridiumNotifier.txt', 'r') as inputFile:
    passes = inputFile.read().splitlines()
    for irPass in passes:
        passDate, passHour, passMin, passMag, where2See = irPass.split('|')
        if int(passDate) == int(thisDay) and int(thisHour) == int(passHour):
            if system() == 'Darwin':
                Notifier.notify("At " + str(passHour) + ": " + str(passMin) +
                        '\n' + "Intensity: " + passMag + '\n' + where2See,
                        title='Iridium Flare'
                )
            else:
                n = pynotify.Notification("Iridium Flare",
                    "At " + str(passHour) + ": " + str(passMin) + '\n' + "Intensity: " + passMag + '\n' + where2See
                )
                n.show()
