import webapp2

from emailsender import EmailSender
from review import ReviewHandler
from new import NewHandler

app = webapp2.WSGIApplication([
    ('/', ReviewHandler),
    ('/nuevo', NewHandler)
], debug=True)
