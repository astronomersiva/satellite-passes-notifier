satellite-passes-notifier
=========================

Pop up notifications for Ubuntu if there is an ISS pass or Iridium flare in the next one hour

####Requirements

* **PyNotify** Use `sudo pip install pynotify`
* **Mechanize** Use `sudo pip install mechanize`
* **Beautiful Soup** Use `sudo pip install beautifulsoup`

####Setup

1. Specify your [heavens-above.com](http://www.heavens-above.com) credentials in the iridiumFetcher.py file.
2. Add the two Python scripts to Crontab using the following steps:
  1. Terminal -> crontab -e
  2. `0 * * * * env DISPLAY=:0 /usr/bin/python /home/userName/cronIridium.py`
  3. `@reboot /usr/bin/python /home/userName/iridiumFetcher.py &`

This is how the notification for Iridium flares look like.
![ScreenShot](https://raw.github.com/astronomersiva/satellite-passes-notifier/master/iridiumPass.png)




