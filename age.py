import re
from datetime import *
from agedata import AgeData, ReleaseItem

"""
TODO:
 ...match against a linear regression

 ...Pull in a whole bunch of UAs from here: 
    See this: http://www.useragentstring.com/pages/All/
    And automate some testing for coverage

 ... Cache arrays

 ... More details in dicts

 ... Hello world page at browserage.com

"""

class Age(object):
	""" Assign Ua """
	def __init__(self, ua):
		self.ua = ua.lower()

	def getAge(self):
		uAgent = self.getUa()
		if not uAgent:
			return None
		return uAgent.getAge()

	def getUa(self):
		if 'chrome' in self.ua:
			return UaChrome(self.ua)
		elif 'firefox' in self.ua:
			return UaFirefox(self.ua)
		elif 'msie' in self.ua:
			return UaMsie(self.ua)
		elif 'opera' in self.ua:
			return UaOpera(self.ua)
		elif 'safari' in self.ua:
			return UaSafari(self.ua)
		elif 'webkit' in self.ua:
			return UaSafari(self.ua)
		return None


class Ua(object):
	""" Get Version Elements and return age results """
	def __init__(self, ua):
		self.ua = ua
		self.ageData = None

	def getReleaseDate(self):
		return 0

	def getAge(self):
		rd = self.getReleaseDate()
		if not rd:
			return None
		return datetime.now().date() - rd

class UaChrome(Ua):
	def __init__(self, ua):
		super(UaChrome, self).__init__(ua)
		self.ageData = AgeData('age-chrome.json')
		self.ageData.load()

	def getReleaseDate(self):
		# http://www.oldapps.com/google_chrome.php
		matches = re.compile('chrome/[a-z0-9\.]*').search(self.ua)
		if not matches:
			return None
		self.verfull = matches.group().split('/')
		self.vernums = self.verfull[1].split('.')

		return self.ageData.getDate(self.vernums)

class UaFirefox(Ua):
	def __init__(self, ua):
		super(UaFirefox, self).__init__(ua)
		self.ageData = AgeData('age-firefox.json')
		self.ageData.load()

	def getReleaseDate(self):
		# https://wiki.mozilla.org/Releases/Old/2011 
		matches = re.compile('firefox/[a-z0-9\.]*').search(self.ua)
		if not matches:
			return None
		self.verfull = matches.group().split('/')
		self.vernums = self.verfull[1].split('.')

		return self.ageData.getDate(self.vernums)

class UaMsie(Ua):
	def __init__(self, ua):
		super(UaMsie, self).__init__(ua)
		self.ageData = AgeData('age-msie.json')
		self.ageData.load()

	def getReleaseDate(self):
		"""http://en.wikipedia.org/wiki/Timeline_of_web_browsers"""
		matches = re.compile('msie [a-z0-9\.]*').search(self.ua)
		if not matches:
			return None
		self.verfull = matches.group().split(' ')
		self.vernums = self.verfull[1].split('.')
		return self.ageData.getDate(self.vernums)

class UaSafari(Ua):

	def __init__(self, ua):
		super(UaSafari, self).__init__(ua)
		self.ageData = AgeData('age-webkit.json')
		self.ageData.load()

	def getReleaseDate(self):
		""" http://en.wikipedia.org/wiki/Safari_version_history """
		matches = re.compile('safari/[a-z0-9\.]*').search(self.ua)
		if not matches:
			return None
		self.verfull = matches.group().split('/')
		self.vernums = self.verfull[1].split('.')

		return self.ageData.getDate(self.vernums)

class UaOpera(Ua):
	
	def __init__(self, ua):
		super(UaOpera, self).__init__(ua)
		self.ageData = AgeData('age-opera.json')
		self.ageData.load()

	def getReleaseDate(self):
		""" http://www.opera.com/docs/history/#o1202 """
		matches = re.compile('version/[a-z0-9\.]*').search(self.ua)
		if not matches:
			return None
		self.verfull = matches.group().split('/')
		self.vernums = self.verfull[1].split('.')
		
		return self.ageData.getDate(self.vernums)

