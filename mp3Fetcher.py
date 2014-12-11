from bs4 import BeautifulSoup
import StringIO
import urllib2
import requests
import zipfile
import os
import sys
import re

def getSize(href):
   downloadInfo = requests.head(href).headers
   downloadSize = int(downloadInfo['content-length']) / (1024 * 1024)
   return str(downloadSize) + "MB"

#Progress bar found on this Stack Overflow question
#http://stackoverflow.com/questions/5783517/downloading-progress-bar-urllib2-python
def chunk_report(bytes_so_far, chunk_size, total_size):
   percent = float(bytes_so_far) / total_size
   percent = round(percent*100, 2)
   sys.stdout.write("Downloaded %d of %d bytes (%0.2f%%)\r" % 
       (bytes_so_far, total_size, percent))

   if bytes_so_far >= total_size:
      sys.stdout.write('\n')

def chunk_read(response, chunk_size=4096, report_hook=None):
   total_size = response.info().getheader('Content-Length').strip()
   total_size = int(total_size)
   bytes_so_far = 0
   data = []

   while 1:
      chunk = response.read(chunk_size)
      bytes_so_far += len(chunk)

      if not chunk:
         break

      data += chunk
      if report_hook:
         report_hook(bytes_so_far, chunk_size, total_size)

   return "".join(data)

if __name__ == '__main__':
    movie = raw_input("Enter the movie name\t").lower()
    year = raw_input("Enter the year of release\t")
    try:
       print "Songs will be downloaded to " + os.getcwd() + '/' + movie 
       os.mkdir(movie)
       os.chdir(movie)
    except:
       os.chdir(movie)
    if int(year) >= 2014:
       base = "http://www.songspk.name/indian-mp3-songs/"
       toAppend = '-'.join(movie.split()) + '-' + year + '-mp3-songs.html'
       songsPKUrl = base + toAppend
    elif int(year) >= 2011:
       base = "http://www.songspk.name/indian-mp3-songs/"
       toAppend = '_'.join(movie.split()) + '_' + year + '_mp3_songs.html'
       songsPKUrl = base + toAppend
    else:
       base = "http://www.songspk.name/indian/"
       toAppend = '_'.join(movie.split()) + '_' + year + '.html'
       songsPKUrl = base + toAppend
    try:
       sourceSite = urllib2.urlopen(songsPKUrl)
    except:
       try:
          #format for albums from early 2010 and before
          base = "http://www.songspk.name/indian/"
          toAppend = '_'.join(movie.split()) + '.html'
          songsPKUrl = base + toAppend
          sourceSite = urllib2.urlopen(songsPKUrl)
       except:
          print songsPKUrl
          print "Link does not exist."
          print "Cleaning up"
          os.chdir('../')
          os.rmdir(movie)
          sys.exit(1)
    soup = BeautifulSoup(sourceSite)
    zipLinks = []
    for link in soup.find_all('a'):
        href = link.get('href')
        try:
            if href.endswith('.zip'):
                zipLinks.append(href)
        except:
            pass
            
    print "Please wait while the download links are fetched."
    counter = 1
    for zip in zipLinks:
        print str(counter) + '\t' + re.findall('\d+Kbps', zip)[0] + '\t' + getSize(zip)
        counter += 1
    
    choice = int(raw_input("Which of the above do you wish to download?")) - 1
    print "Press y/n to confirm."
    proceed = raw_input().lower()
    if proceed == 'n':
       print "Cleaning up and exiting."
       os.chdir('../')
       os.rmdir(movie)
       sys.exit(1)
    print "Downloading...Please wait"
    downloadFileReq = urllib2.Request(zipLinks[choice], headers={'User-Agent': "Magic"})
    downloadFile = urllib2.urlopen(downloadFileReq)
    downloaded = chunk_read(downloadFile, report_hook=chunk_report)
    zipFile = zipfile.ZipFile(StringIO.StringIO(downloaded))
    print "The following songs have been downloaded."
    try:
        for song in zipFile.namelist():
            print song
    except:
        pass    
    print "Extracting all songs to the directory " + os.getcwd()     
    zipFile.extractall()    
    print "Download successful."

