import mechanize
from time import strftime
from bs4 import *
from datetime import datetime, date, timedelta
from time import strptime
from getopt import getopt
import os, sys, envoy

thisDate = date.today()
thisYear = thisDate.year
thisMonth = thisDate.strftime("%b")

# Parse a row of Heavens Above data and return the start date (datetime),
# the intensity (integer), and the beginning, peak, and end sky positions
# (strings).
def parseRow(row):
  cols = row.findAll('td')
  dStr = cols[0].a.string
  # dStr is in the form 31 Dec. To parse the date with strptime,
  # the day must have a leading zero if it doesn't have one. Also,
  # we need to add the year, being careful when the year changes.
  dStrList =dStr.split()
  if len(dStrList[0]) < 2:
    dStrList[0] = '0' + dStrList[0]
  if dStrList[1] == 'Jan' and thisMonth == 'Dec':
    dStrList.append(str(thisYear+1))
  else:
    dStrList.append(str(thisYear))
  dStr = ' '.join(dStrList)
  t1Str = ':'.join(cols[2].string.split(':')[0:2])
  t3Str = ':'.join(cols[8].string.split(':')[0:2])
  intensity = float(cols[1].string)
  alt1 = cols[3].string.replace(u'ﾰ', ' degrees')
  az1 = cols[4].string
  alt2 = cols[6].string.replace(u'ﾰ', ' degrees')
  az2 = cols[7].string
  alt3 = cols[9].string.replace(u'ﾰ', ' degrees')
  az3 = cols[10].string
  loc1 = '%s %s' % (az1, alt1)
  loc2 = '%s %s' % (az2, alt2)
  loc3 = '%s %s' % (az3, alt3)
  startStr = '%s %s' % (dStr, t1Str)
  start = datetime(*strptime(startStr, '%d %b %Y %H:%M')[0:7])
  endStr = '%s %s' % (dStr, t3Str)
  end = datetime(*strptime(endStr, '%d %b %Y %H:%M')[0:7])
  return (start, end, intensity, loc1, loc2, loc3)


# Parse command line options.
justPrint = False
optlist, args = getopt(sys.argv[1:], 'ph')
for o, a in optlist:
  if o == '-p':
    justPrint = True
  else:
    print usage
    sys.exit()


# Heavens Above URLs and login information.
loginURL = 'http://heavens-above.com/login.aspx'
issURL = 'http://www.heavens-above.com/PassSummary.aspx?satid=25544'

# Create virtual browser and login.
br = mechanize.Browser()
br.set_handle_robots(False)
br.open(loginURL)
br.select_form(nr=0)    # the login form is the first on the page
br['ctl00$cph1$Login1$UserName'] = 'astronomersiva'
br['ctl00$cph1$Login1$Password'] = 'fUTR5dru'
resp = br.submit()

# Get the 10-day ISS page.
iHtml = br.open(issURL).read()



# In the past, Beautiful Soup hasn't been able to parse the Heavens Above HTML.
# To get around this problem, we extract just the table of ISS data and set
# it in a well-formed HTML skeleton. If there is no table of ISS data, create
# an empty table.
try:
    table = iHtml.split(r'<table class="standardTable"', 1)[1]
    table = table.split(r'>', 1)[1]
    table = table.split(r'</table>', 1)[0]
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
rows = soup.findAll('table')[0].findAll('tr')[2:]


with open('ISSNotifier.txt', 'w') as file:
    for row in rows:
        (start,end,magnitude,rise,maxvis,sett) = parseRow(row)
        passDate, passHour, passMin, passMag, where2See = start.strftime('%d'), start.strftime('%H'),start.strftime('%M'), str(magnitude), rise
        details = [passDate, passHour, passMin, passMag, where2See]
        file.writelines('|'.join(details))       
       
  
  
