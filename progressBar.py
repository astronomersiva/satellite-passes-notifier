import urllib2, sys

def chunk_report(bytes_so_far, chunk_size, total_size):
   percent = float(bytes_so_far) / total_size
   percent = round(percent*100, 2)
   sys.stdout.write("Downloaded %d of %d bytes (%0.2f%%)\r" % 
       (bytes_so_far, total_size, percent))

   if bytes_so_far >= total_size:
      sys.stdout.write('\n')

def chunk_read(response, chunk_size=8192, report_hook=None):
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
    url = 'http://www.songspk320net.us/128/indian/Ungli-128Kbps-2014(Songs.PK).zip'
    req = urllib2.Request(url, headers={'User-Agent': "Magic"})
    response = urllib2.urlopen(req)
    chunk_read(response, report_hook=chunk_report)
