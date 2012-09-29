import sys
from agedata import AgeData
import re
from datetime import *

class BrowserParser(object):
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

class BrpChrome(BrowserParser):

	def __init__(self):
		super(BrpChrome, self).__init__()
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

class BrpFirefox(BrowserParser):

	def __init__(self):
		super(BrpFirefox, self).__init__()
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

class BrpMsie(BrowserParser):

	def __init__(self):
		super(BrpMsie, self).__init__()
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

class BrpOpera(BrowserParser):

	def __init__(self):
		super(BrpOpera, self).__init__()
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

class BrpSafari(BrowserParser):

	def __init__(self):
		super(BrpSafari, self).__init__()
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

class BrpWebkit(BrowserParser):

	def __init__(self):
		super(BrpWebkit, self).__init__()
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

