import re
from datetime import *
from agedata import AgeData, ReleaseItem
#from httpagentparser as hap
import sys

"""
TODO:
 ...match against a linear regression

 ... Cache arrays

 ... More details in dicts

 ... Hello world page at browserage.com

"""

class Age(object):
	""" Assign Ua """
	parsers = None
	def __init__(self, ua):
		self.raw_ua = ua.lower()
		if not Age.parsers:
			Age.registerParsers()

		self.ua = None
		for uap in Age.parsers:
			if uap.doesMatch(self.raw_ua):
				self.ua = uap
				break

	def getAge(self):
		if not self.ua:
			return None
		return self.ua.getAge(self.raw_ua)

	def getBrowser(self):
		return ua.getBrowser()

	@staticmethod
	def registerParsers():
		Age.parsers = [c() for c in globals().values() if Ua in getattr(c, '__mro__', [])]
		Age.parsers.sort(key=lambda p: p.getParseOrder())
       
	def getUa(self):
		return self.ua

class Ua(object):
	""" Get Version Elements and return age results """
	def __init__(self):
		self.ageData = None

	def getParseOrder(self):
		return sys.maxint

	def doesMatch(self, ua):
		return False

	def getReleaseDate(self):
		return 0

	def getBrowser(self):
		return ''

	def getAge(self, ua):
		rd = self.getReleaseDate(ua)
		if not rd:
			return None
		return datetime.now().date() - rd

class UaChrome(Ua):

	def __init__(self):
		super(UaChrome, self).__init__()
		self.ageData = AgeData('age-chrome.json', propLimit=0)

	def getParseOrder(self):
		return 1

	def doesMatch(self, ua):
		return ua and 'chrome' in ua

	def getBrowser(self):
		return 'chrome'

	def getReleaseDate(self, ua):
		# http://www.oldapps.com/google_chrome.php
		matches = re.compile('chrome/[a-z0-9\.]*').search(ua)
		if not matches:
			return None
		self.verfull = matches.group().split('/')
		self.vernums = self.verfull[1].split('.')

		return self.ageData.getDate(self.vernums)

class UaFirefox(Ua):

	def __init__(self):
		super(UaFirefox, self).__init__()
		self.ageData = AgeData('age-firefox.json')

	def getParseOrder(self):
		return 2

	def doesMatch(self, ua):
		return ua and 'firefox' in ua

	def getBrowser(self):
		return 'firefox'

	def getReleaseDate(self, ua):
		# https://wiki.mozilla.org/Releases/Old/2011 
		matches = re.compile('firefox/[a-z0-9\.]*').search(ua)
		if not matches:
			return None
		self.verfull = matches.group().split('/')
		self.vernums = self.verfull[1].split('.')

		return self.ageData.getDate(self.vernums)

class UaMsie(Ua):

	def __init__(self):
		super(UaMsie, self).__init__()
		self.ageData = AgeData('age-msie.json')

	def getParseOrder(self):
		return 3

	def doesMatch(self, ua):
		return ua and 'msie' in ua

	def getBrowser(self):
		return 'msie'

	def getReleaseDate(self, ua):
		"""http://en.wikipedia.org/wiki/Timeline_of_web_browsers"""
		matches = re.compile('msie [a-z0-9\.]*').search(ua)
		if not matches:
			return None
		self.verfull = matches.group().split(' ')
		self.vernums = self.verfull[1].split('.')
		return self.ageData.getDate(self.vernums)

class UaOpera(Ua):

	def __init__(self):
		super(UaOpera, self).__init__()
		self.ageData = AgeData('age-opera.json')

	def getParseOrder(self):
		return 4

	def doesMatch(self, ua):
		return ua and 'opera' in ua

	def getBrowser(self):
		return 'opera'

	def getReleaseDate(self, ua):
		""" http://www.opera.com/docs/history/#o1202 """
		matches = re.compile('version/[a-z0-9\.]*').search(ua)
		if not matches:
			return None
		self.verfull = matches.group().split('/')
		self.vernums = self.verfull[1].split('.')
		
		return self.ageData.getDate(self.vernums)

class UaSafari(Ua):

	def __init__(self):
		super(UaSafari, self).__init__()
		self.ageData = AgeData('age-safari.json')

	def getParseOrder(self):
		return 5

	def doesMatch(self, ua):
		return ua and 'safari' in ua

	def getBrowser(self):
		return 'safari'

	def getReleaseDate(self, ua):
		""" http://en.wikipedia.org/wiki/Safari_version_history """
		#matches = re.compile('safari/[a-z0-9\.]*').search(ua)
		matches = re.compile('version/[a-z0-9\.]*').search(ua)
		if not matches:
			return None
		self.verfull = matches.group().split('/')
		self.vernums = self.verfull[1].split('.')

		return self.ageData.getDate(self.vernums)

class UaWebkit(Ua):

	def __init__(self):
		super(UaWebkit, self).__init__()
		self.ageData = AgeData('age-webkit.json')

	def getParseOrder(self):
		return 6

	def doesMatch(self, ua):
		return ua and 'webkit' in ua

	def getBrowser(self):
		return 'webkit'

	def getReleaseDate(self, ua):
		""" http://en.wikipedia.org/wiki/Safari_version_history """
		matches = re.compile('safari/[a-z0-9\.]*').search(ua)
		if not matches:
			return None
		self.verfull = matches.group().split('/')
		self.vernums = self.verfull[1].split('.')

		return self.ageData.getDate(self.vernums)