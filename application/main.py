import json

from google.appengine.ext import ndb
import webapp2

from base_handler import BaseHandler


KEY_MAP = {
    16: 'sweet16',
    8: 'elite8',
    7: 'last7',
    6: 'last6',
    5: 'last5',
    4: 'final4',
}
USER_PATHS = '|'.join(
    [value for value in KEY_MAP.itervalues() if value != KEY_MAP[16]])
USER_PATHS_ROUTE = '/(%s)' % (USER_PATHS,)



class BracketContainer(ndb.Model):
    year = ndb.IntegerProperty(required=True, indexed=False)
    bracket = ndb.PickleProperty()
    scenarios = ndb.StringProperty(indexed=False)

    @classmethod
    def get_or_insert_n(cls, n):
        return cls.get_or_insert(KEY_MAP[n])


class MainPage(BaseHandler):

    def get(self):
        self.render_response('main.templ')


class ShowUserData(BaseHandler):

    def get(self, key):
        self.response.headers['Content-Type'] = 'text/plain'
        bracket_container = BracketContainer.get_or_insert(key)
        if bracket_container.scenarios is not None:
            self.response.write(bracket_container.scenarios)
        else:
            self.response.write('Not ready yet')


class RedirectHandler(webapp2.RequestHandler):

    def get(self):
        self.redirect('/')


routes = [
    (USER_PATHS_ROUTE, ShowUserData),
    ('/', MainPage),
    ('/.*', RedirectHandler),
]
app = webapp2.WSGIApplication(routes, debug=True)
