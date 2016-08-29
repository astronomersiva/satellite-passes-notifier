#!/usr/bin/python
# -*- coding: UTF-8 -*-

import mechanize
from time import strftime
from BeautifulSoup import BeautifulSoup
from datetime import datetime, date, timedelta
from time import strptime
from getopt import getopt
import os, sys
import pynotify

# Since Heavens Above stopped including the year in the flare
# dates, we have to figure it out ourselves. Easy enough most
# of the year, a little tricky when the week spans a change of
# year.
thisDateTime = datetime.now()
thisYear = thisDateTime.year
thisMonth = thisDateTime.strftime("%b")
thisDay = thisDateTime.day
thisHour = thisDateTime.hour
thisMin = thisDateTime.strftime("%M")

# Parse a row of Heavens Above data and return the start date (datetime),
# the intensity (integer), and the sky position (string).
def parseRow(row):
  cols = row.findAll('td')
  dtStr = cols[0].a.string
  # dtStr is in the form Jan 1, 01:00:00. To parse the date with
  # strptime, the day must have a leading zero if it's < 10. Also,
  # we need to add the year, being careful when the year changes.
  dtStrList =dtStr.split()
  if len(dtStrList[1]) < 3:
    dtStrList[1] = '0' + dtStrList[1]
  if dtStrList[0] == 'Jan' and thisMonth == 'Dec':
    dtStrList.insert(2, str(thisYear+1))
  else:
    dtStrList.insert(2, str(thisYear))
  dtStr = ' '.join(dtStrList)
  intensity = float(cols[1].string)
  alt = cols[2].string.replace('&#176;', '')
  az = cols[3].string.replace('&#176;', '')
  loc = 'alt %s, az %s' % (alt, az)
  start = datetime(*strptime(dtStr, '%b %d, %Y %H:%M:%S')[0:7])
  return (start, intensity, loc)


# Heavens Above URLs and login information.
lURL = 'http://heavens-above.com/login.aspx'                       # login
iURL = 'http://heavens-above.com/IridiumFlares.aspx?Session='     # iridium flares

# Create virtual browser and login.
br = mechanize.Browser()
br.set_handle_robots(False)
br.open(lURL)
br.select_form(nr=0)    # the login form is the first on the page
br['ctl00$cph1$Login1$UserName'] = 'username'
br['ctl00$cph1$Login1$Password'] = 'password'
resp = br.submit()


# Get the 7-day Iridium page.
iHtml = br.open(iURL).read()


# For some reason, Beautiful Soup can't parse the HTML on the Iridium page.
# To get around this problem, we extract just the table of flare data and set
# it in a well-formed HTML skeleton. If there is no table of flare data, create
# an empty table.
try:
  table = iHtml.split(r'<table class="standardTable"')[1]
  table = table.split(r'</table>')[0]
except IndexError:
  table = '<tr><td></td></tr>'


html = '''<html>
<head>
</head>
<body>
<table>
%s
</table>
</body>
</html>''' % table

# Parse the HTML.
soup = BeautifulSoup(html)

# Collect only the data rows of the table.
rows = soup.findAll('table')[0].findAll('tr')[1:]

# Go through the data rows, adding only bright evening events to my "home" calendar.
with open('IridiumNotifier.txt', 'w') as file:
    for row in rows:
        (start, intensity, loc) = parseRow(row)
        passDate, passHour, passMin, passMag, where2See = start.strftime('%d'), start.strftime('%H'), start.strftime('%M'), str(intensity), loc.encode('utf-8')
        details = [passDate, passHour, passMin, passMag, where2See]
        file.write(('|').join(details) + '\n')
