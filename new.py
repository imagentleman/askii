import os
from datetime import datetime
import json

import webapp2
import jinja2

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.api import mail


class NewHandler(webapp2.RequestHandler):

  def post(self):
    title = self.request.get('title')
    tag = self.request.get('tag')
    desc = self.request.get('desc')

    user = users.get_current_user()

    if not title or not tag or not desc or not user:
      self.error(400)

    story = Story(author=user.email(), title=title, tag=tag, desc=desc, audience=[user.email()])
    key = story.put()
    self.response.headers['Content-Type'] = 'application/json'

    if key:
      jinja_environment = jinja2.Environment(
        loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))
      template = jinja_environment.get_template('mail_template.html')
      email_body = template.render({'id': key.id(), 'title': title, 'desc': desc})

      message = mail.EmailMessage(
          sender = user.email(),
          to = user.email(),
          subject = 'Por favor califica esto',
          html = email_body)

      try:
        message.send()
        self.response.out.write(json.dumps({'error': False}))
      except:
        self.error(500)

    else:
      self.response.out.write(json.dumps({'error': True}))

  def get(self):
    user = users.get_current_user()
    if not user:
      self.redirect(users.create_login_url(self.request.uri))
      return

    jinja_environment = jinja2.Environment(
        loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
        extensions=['jinja2.ext.autoescape'],
        autoescape=True)
    template = jinja_environment.get_template('nuevo.html')
    now = datetime.now().date()
    self.response.write(template.render({'email': user.email(), 'date': now}))

class Story(db.Model):
    author = db.StringProperty(required=True)
    title = db.TextProperty(required=True)
    desc = db.TextProperty(required=True)
    tag = db.StringProperty(required=True)
    audience = db.StringListProperty(required=True)
    date = db.DateProperty(auto_now_add=True)