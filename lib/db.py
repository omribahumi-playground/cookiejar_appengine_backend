from google.appengine.ext import db
from google.appengine.api import users

class Cookie(db.Model):
    author = db.UserProperty()
    content = db.TextProperty()
    description = db.StringProperty()
    date = db.DateTimeProperty(auto_now_add=True)

__all__ = ['Cookie']
