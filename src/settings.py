from os.path import dirname, realpath
from jinja2 import Environment, FileSystemLoader
from google.appengine.ext import ndb


DEBUG = True

SECRET_KEY = 'asdfjasdflkjsfewi23kjl3kjl45kjl56jk6hjb76vsjsa'

CONFIG = {
}


SRC_ROOT = dirname(realpath(__file__))

JINJA_ENVIRONMENT = Environment(
    loader=FileSystemLoader(SRC_ROOT),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True,
)

REGIONS = ['NSW', 'VIC', 'QLD', 'WA', 'SA', 'TAS', 'ACT', 'NT']

PARENT_KEY = ndb.Key('daddy', 'oz')