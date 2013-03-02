import webapp2
import json
from datetime import datetime
from google.appengine.api import users
from lib.db import *

class WhoAmIHandler(webapp2.RequestHandler):
    def get(self):
        """Return the currently logged in username"""
        user = users.get_current_user()
        if user:
            self.response.write(user.nickname())

class CookieHandler(webapp2.RequestHandler):
    def get(self):
        """Returns a JSON with all cookies"""
        data = [{
                    'id': cookie.key().id(),
                    'author' : cookie.author.nickname(),
                    'description' : cookie.description,
                    'date' : str(cookie.date)
                }
                for cookie in Cookie.all()]
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(data))

    def post(self):
        """Create a new cookie"""
        user = users.get_current_user()

        self.response.headers['Content-Type'] = 'application/json'
        cookie = Cookie(author=user,
                        description=self.request.get('description'),
                        content=self.request.get('content'))
        cookie.put()
        self.response.out.write(json.dumps({'id' : cookie.key().id()}))

class CookieIdHandler(webapp2.RequestHandler):
    def get(self, id):
        """Return a JSON representation of a single cookie"""
        self.response.headers['Content-Type'] = 'application/json'
        cookie = Cookie.get_by_id(int(id))

        if not cookie:
            self.response.status = 404
            self.response.out.write(json.dumps(
                {'error' : 'Cookie id %s not found' % (id,)}))
        else:
            data = {
                'id' : cookie.key().id(),
                'author' : cookie.author.nickname(),
                'description' : cookie.description,
                'content' : cookie.content,
                'date' : str(cookie.date)
            }

            self.response.out.write(json.dumps(data))

    def post(self, id):
        """Update cookie"""
        self.response.headers['Content-Type'] = 'application/json'
        user = users.get_current_user()
        cookie = Cookie.get_by_id(int(id))

        if not cookie:
            self.response.status = 404
            self.response.out.write(json.dumps(
                {'error' : 'Cookie id %s not found' % (id,)}))
        elif cookie.author != user:
            self.response.status = 400
            self.response.out.write(json.dumps(
                {'error' : 'You are not the creator of cookie id  %s' % (id,)}))
        else:
            if self.request.get('description', None) != None:
                cookie.description = self.request.get('description')
            if self.request.get('content', None) != None:
               cookie.content = self.request.get('content')
            cookie.date = datetime.now()
            cookie.put()
            self.response.out.write(json.dumps({'id' : cookie.key().id()}))

    def delete(self, id):
        """Delete cookie"""
        self.response.headers['Content-Type'] = 'application/json'
        user = users.get_current_user()
        cookie = Cookie.get_by_id(int(id))

        if not cookie:
            self.response.status = 404
            self.response.out.write(json.dumps(
                {'error' : 'Cookie id %s not found' % (id,)}))
        elif cookie.author != user:
            self.response.status = 400
            self.response.out.write(json.dumps(
                {'error' : 'You are not the creator of cookie id  %s' % (id,)}))
        else:
            cookie.delete()
            self.response.out.write(json.dumps({'id' : cookie.key().id()}))

app = webapp2.WSGIApplication([('/api/whoami', WhoAmIHandler),
                               ('/api/cookie', CookieHandler),
                               ('/api/cookie/(\d+)', CookieIdHandler)],
                              debug=True)
