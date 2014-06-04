import jinja2
import os
import webapp2

from google.appengine.api import mail
from google.appengine.api import users

from urlparse import urlparse

class EmailSender(webapp2.RequestHandler):

  def get(self):
    # require users to be logged in to send emails
    user = users.get_current_user()
    if not user:
      self.redirect(users.create_login_url(self.request.uri))
      return

    email = user.email()

    # the review url corresponds to the App Engine app url
    pr = urlparse(self.request.url)
    review_url = '%s://%s' % (pr.scheme, pr.netloc)

    # load the email template and replace the placeholder with the review url
    jinja_environment = jinja2.Environment(
        loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))
    template = jinja_environment.get_template('mail_template.html')
    email_body = template.render({'review_url': review_url})

    message = mail.EmailMessage(
        sender = email,
        to = email,
        subject = 'Please review Google Cafe',
        html = email_body)

    try:
      message.send()
      self.response.write('OK')
    except:
      self.error(500)
