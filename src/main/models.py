from google.appengine.ext import ndb
from src.settings import REGIONS


class House(ndb.Model):
    region = ndb.StringProperty(required=True, choices=REGIONS)
    url = ndb.StringProperty(required=True)
    name = ndb.StringProperty(default='')
    title = ndb.StringProperty(default='')
    description = ndb.StringProperty(default='')
    bedrooms = ndb.IntegerProperty()
    bathrooms = ndb.IntegerProperty()
    car_spaces = ndb.IntegerProperty()
    agent = ndb.StringProperty(default='')
    img = ndb.StringProperty(default='')
    info = ndb.StringProperty(default='')
    price = ndb.IntegerProperty()
    created_at = ndb.DateTimeProperty(auto_now_add=True)
    updated_at = ndb.DateTimeProperty(auto_now=True)

    def __unicode__(self):
        return self.name