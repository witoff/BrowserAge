import re
from datetime import *

"""
TODO:
 1. Pull in a whole bunch of UAs from here: 
    See this: http://www.useragentstring.com/pages/All/
    And automate some testing for coverage
 2. Find a better syntax than all these if statements
 	...framework that takes an array of vers, and returns best base match
	Add MSIE
	Add Opera

"""

class Age(object):
	
	def __init__(self, ua):
		self.ua = ua

	def getBrowser(self):
		if 'Chrome' in self.ua:
			return UaChrome(self.ua)
		elif 'Firefox' in self.ua:
			return UaFirefox(self.ua)
		elif 'MSIE' in self.ua:
			return UaMsie(self.ua)
		elif 'Safari' in self.ua:
			return UaSafari(self.ua)



class Ua(object):
	def __init__(self, ua):
		self.ua = ua

	def getReleaseDate(self):
		return 0

class UaChrome(Ua):
	def getReleaseDate(self):
		# http://www.oldapps.com/google_chrome.php
		matches = re.compile('Chrome/[0-9\.]*').search(self.ua)
		if not matches:
			return None
		self.verfull = matches.group().split('/')
		self.vernums = self.verfull[1].split('.')
		mj = int( self.vernums[0] )

		if mj==1:
			return date(2009, 4, 24)
		if mj==2:
			return date(2009,6,10)
		if mj==3:
			return date(2009,7,13)
		if mj==4:
			return date(2009,10,24)
		if mj==5:
			return date(2010,1,30)
		if mj==6:
			return date(2010,8,12)
		if mj==7:
			return date(2010,10,19)
		if mj==8:
			return date(2010,12,2)
		if mj==9:
			return date(2011,2,2)
		if mj==10:
			return date(2011,3,8)
		if mj==11:
			return date(2011,5,6)
		if mj==12:
			return date(2011,6,6)
		if mj==13:
			return date(2011,7,20)
		if mj==14:
			return date(2011,9,16)
		if mj==15:
			return date(2011,10,26)
		if mj==16:
			return date(2011,12,1)
		if mj==17:
			return date(2012,2,17)
		if mj==18:
			return date(2012,3,28)
		if mj==19:
			return date(2012,5,23)
		if mj==20:
			return date(2012,6,28)
		if mj>=21:
			return date(2012,7,31)
		return None

class UaFirefox(object):
	def getReleaseDate(self):
		# https://wiki.mozilla.org/Releases/Old/2011 
		matches = re.compile('Firefox/[a-zA-Z0-9\.]*').search(self.ua)
		if not matches:
			return None
		self.verfull = matches.group().split('/')
		self.vernums = self.verfull[1].split('.')
		mj = int( self.vernums[0] )

		if mj==1:
			return date(2009, 4, 24)

class UaMsie(object):
	"""http://en.wikipedia.org/wiki/Timeline_of_web_browsers"""
	def getReleaseDate(self):
		return 0

class UaSafari(object):
	def getReleaseDat(self):
		# from http://en.wikipedia.org/wiki/Safari_version_history
		return 0

class UaOpera(object):
	def getReleaseDat(self):
		# from 
		return 0
