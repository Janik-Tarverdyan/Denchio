import imp
import os
import sys


sys.path.insert(0, os.path.dirname(__file__))

wsgi = imp.load_source('wsgi', './Denchio/wsgi.py')
# wsgi = imp.load_source('wsgi', '/home/dencsfav/denchio/Denchio/wsgi.py')
application = wsgi.application
