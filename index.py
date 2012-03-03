# vim: set fileencoding=utf-8 :

#    fwd4lang - Forward URL for your Language
#    It's based on "HelloWeb", Copyright (C) 2008  Sergey Astanin.
#    Copyright (C) 2012 Yishin Li
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import re

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import logging

def parse_accept_language(accept_language):
	"Parse Accept-Language header. See RFC2616, sec. 14."
	if not accept_language: return []
	ll=[ v.strip().split(';') for v in accept_language.split(',') ]
	ll=[ len(l)==1 and l.append(1.0) or l for l in ll]
	ll=[ [l[0],float(re.sub('q\s*=\s*','',str(l[1])))] for l in ll]
	ll=[ l[0] for l in sorted(ll,lambda l1,l2: l1[1] > l2[1]) ]
	ll=[ re.sub('-','_',l).lower() for l in ll ]
	return ll 

class MainPage(webapp.RequestHandler):
	@staticmethod
	def languages(request):
		al=request.headers.get('Accept-Language')
		return parse_accept_language(al)

	def get(self,action=''):
            lang = self.languages(self.request)
            logging.debug('lang='+lang[0])
            if (re.match("^en", lang[0]) != None):
                url='http://en.araisrobo.com/'
            elif (re.match("^zh", lang[0]) != None):
                url='http://zh-tw.araisrobo.com/'
            else:
                # default to english
                url='http://en.araisrobo.com/'
	    self.redirect(url)

application = webapp.WSGIApplication(
                                     [(r'/(.*)', MainPage)], 
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
	main()
