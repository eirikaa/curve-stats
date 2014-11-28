# -*- coding: utf-8 -*-

import webapp2
import os
import jinja2
import urllib2
import operator

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainPage(webapp2.RequestHandler):
    def get(self):

        ranks = {'geod2ECEF': '',
                 'KVALBERDILDOEDalne': '',
                 'das grose dildo': '',
                 'mobyduck': '',
                 'ECEF2geod': '',
                 'ullerudflaket': '',
                 'Brettet': '',
                 'kingkooy': '',
                 'gushiminatoren': '',
                 'inge': '',
                 'jonnamosa': '',
                 'houseparty': '',
                 'gjordis': '',
                 'techniqern': ''}

        for name in ranks.keys():
            if name == 'gjordis':
                response = urllib2.urlopen('http://curvefever.com/users/gjørdis')
            else:
                response = urllib2.urlopen('http://curvefever.com/users/{}'.format(name.replace(' ', '-')))
            html = response.read()
            index = html.find('</dd>\n<dt>Rank</dt>\n<dd>')
            index += 24
            ranks[name] = int(html[index:index+4].replace('<', ''))

        sorted_ranks = sorted(ranks.items(), key=operator.itemgetter(1))
        sorted_ranks.reverse()

        template_values = {'ranks': sorted_ranks, }
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))

application = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)