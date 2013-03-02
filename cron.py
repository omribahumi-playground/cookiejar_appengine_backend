import webapp2
from lib.db import *
from datetime import datetime, timedelta
import logging

class CronCleanupHandler(webapp2.RequestHandler):
    def __init__(self, request, response):
        self.initialize(request, response)
        self.log = logging.getLogger(self.__class__.__name__)

    def get(self):
        self.log.info('Starting cleanup')

        expire = timedelta(hours=8)
        results = Cookie.gql('WHERE date <= :1', datetime.now() - expire)
        results_count = results.count()

        for result in results:
            result.delete()

        self.log.info('Cleanup done! removed %d entities' % (results_count,))

app = webapp2.WSGIApplication([('/cron/cleanup', CronCleanupHandler)],
                              debug=True)
