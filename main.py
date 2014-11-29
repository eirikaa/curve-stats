# -*- coding: utf-8 -*-

import webapp2
import os
import jinja2
import urllib2
import logging

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainPage(webapp2.RequestHandler):
    def get(self):

        ranks = {'geod2ECEF': [],
                 'KVALBERDILDOEDalne': [],
                 'das grose dildo': [],
                 'mobyduck': [],
                 'ECEF2geod': [],
                 'ullerudflaket': [],
                 'Brettet': [],
                 'kingkooy': [],
                 'gushiminatoren': [],
                 'inge': [],
                 'jonnamosa': [],
                 'houseparty': [],
                 'gjordis': [],
                 'techniqern': []}

        for name in ranks.keys():
            if name == 'gjordis':
                response = urllib2.urlopen('http://curvefever.com/users/gjørdis')
            else:
                response = urllib2.urlopen('http://curvefever.com/users/{}'.format(name.replace(' ', '-')))
            html = response.read()
            # Find rank
            index = html.find('</dd>\n<dt>Rank</dt>\n<dd>')
            index += 24
            ranks[name].append(int(html[index:index+4].replace('<', '')))
            # Find last 20 stats
            index = html.find('<tbody>')
            rank_last_20 = 0
            for _ in range(20):
                index = html.find('</a></td><td align="right">FFA</td><td align="right">', index)
                if index == -1:
                    break
                index = html.find('</td> </tr>', index)
                last_game = html[index-4:index]
                last_game = last_game.replace('"', '')
                last_game = last_game.replace('>', '')
                last_game = last_game.replace('t', '')
                try:
                    rank_last_20 += int(last_game)
                except ValueError:
                    logging.info('LOGGING: Last_game = {}, player = {}'.format(last_game, name))
                    break
            if rank_last_20 > 0:
                rank_last_20 = '+' + str(rank_last_20)
            ranks[name].append(rank_last_20)

        players = ((player, ranks[player][0], ranks[player][1]) for player in ranks.keys())
        sorted_players = sorted(players, key=lambda player: player[1])
        sorted_players.reverse()

        template_values = {'ranks': sorted_players, }
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))

application = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)