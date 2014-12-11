import pynotify
pynotify.init("image")

n = pynotify.Notification("Image",
  "Hurray! an Image!",
  "python.png",
)

n.show()
"""import pynotify
pynotify.init("markup")

n = pynotify.Notification("Markup",
  '''
  <b>bold</b>, <i>italic</i>, <u>underline</u>
  and even <a href="http://google.com">links</a> are supported!
  '''
)

n.show()
import pynotify

''' libnotify needs some init value,
it really can be anything, it just uses it
to differentiate between the popups
'''
pynotify.init("Basic")

n = pynotify.Notification("Title",
  "Some sample content"
)

n.show()
"""
