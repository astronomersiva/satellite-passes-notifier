satellite-passes-notifier
=========================

Pop up notifications for Ubuntu if there is an ISS pass or Iridium flare in the next one hour.

[Work in progress](https://github.com/astronomersiva/satellite-passes-notifier/tree/patch_mac_osx) for Mac OS X. Feel free to contribute :)

#### Requirements

Use the terminal to execute these commands.
* **PyNotify** Use `sudo pip install pynotify`
* **pync** Use `sudo pip install pync`
* **Mechanize** Use `sudo pip install mechanize`
* **Beautiful Soup** Use `sudo pip install beautifulsoup`

#### Setup

1. Specify your [heavens-above.com](http://www.heavens-above.com) credentials in the iridiumFetch.py file.
2. Add the two Python scripts to Crontab using the following steps:
  1. Terminal -> crontab -e
  2. Navigate to the bottom of the screen just after the lines that start with # sign.
  3. Enter the following lines.
     1. `0 * * * * env DISPLAY=:0 /usr/bin/python /home/userName/cronIridium.py`
     2. `@reboot /usr/bin/python /home/userName/iridiumFetch.py &`
  4. Ctrl + O write these lines to the Cron table.
  5. Ctrl + X to close the Crontab.

This is how the notification for Iridium flares look like.
![ScreenShot](https://raw.github.com/astronomersiva/satellite-passes-notifier/master/iridiumPass.png)
