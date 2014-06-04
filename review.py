import os

import webapp2
import jinja2

from new import Story
from google.appengine.ext import db

class ReviewHandler(webapp2.RequestHandler):

  def post(self):
    ratingValue = self.request.get('review.reviewRating.ratingValue')
    reviewBody = self.request.get('review.reviewBody')
    id = self.request.get('id')

    if not ratingValue or not id:
      self.error(400)
      return

    review = Review(storyId=id, ratingValue=int(ratingValue), reviewBody=reviewBody)
    review.put()
    return

  def get(self):
    stories = Story.all().fetch(1000)

    results = []

    for s in stories:
      total = 0
      q = Review.all()
      q.filter("storyId =", str(s.key().id()))
      reviews = q.fetch(100)
      for r in reviews:
        total += r.ratingValue
      if len(reviews):
        score = round(float(total) / len(reviews), 2)
      else:
        score = 0

      result = {'score': score, 'title': s.title, 'desc': s.desc, 'tag': s.tag, 'votes': len(reviews), 'author': s.author, 'date': s.date}
      results.append(result)

    jinja_environment = jinja2.Environment(
        loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))
    template = jinja_environment.get_template('home.html')
    self.response.write(template.render({'stories': results}))


class Review(db.Model):
    storyId = db.StringProperty(required=True)
    ratingValue = db.IntegerProperty(required=True)
    reviewBody = db.TextProperty(required=False)
