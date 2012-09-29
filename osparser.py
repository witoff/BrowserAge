import sys
from agedata import AgeData
import re
from datetime import *

class OsParser(object):
	""" Get Version Elements and return age results """
	def __init__(self):
		#'.*\(*(key1)|(key2).*\).*'
		pass

	def getParseOrder(self):
		return sys.maxint

	def doesMatch(self, ua):
		return False

	def getOs(self):
		return ''

class OspWindows(OsParser):

	def __init__(self):
		self.matcher = re.compile('\(.*windows.*\)', re.IGNORECASE)

	def getParseOrder(self):
		return 1

	def doesMatch(self, ua):
		return bool(self.matcher.search(ua))

	def getOs(self):
		return 'windows'

class OspIOS(OsParser):

	def __init__(self):
		self.matcher = re.compile('\(.*(iphone)|(ipad).*\)', re.IGNORECASE)

	def getParseOrder(self):
		return 1

	def doesMatch(self, ua):
		return bool(self.matcher.search(ua))

	def getOs(self):
		return 'ios'

class OspOsx(OsParser):

	def __init__(self):
		self.matcher = re.compile('\(.*macintosh.*\)', re.IGNORECASE)

	def getParseOrder(self):
		return 2

	def doesMatch(self, ua):
		return bool(self.matcher.search(ua))

	def getOs(self):
		return 'osx'

class OspAndroid(OsParser):

	def __init__(self):
		self.matcher = re.compile('\(.*android.*\)', re.IGNORECASE)

	def getParseOrder(self):
		return 1

	def doesMatch(self, ua):
		return bool(self.matcher.search(ua))

	def getOs(self):
		return 'android'

class OspLinux(OsParser):

	def __init__(self):
		self.matcher = re.compile('\(.*.linux*\)', re.IGNORECASE)

	def getParseOrder(self):
		return 2

	def doesMatch(self, ua):
		return bool(self.matcher.search(ua))

	def getOs(self):
		return 'linux'


class OspBB(OsParser):

	def __init__(self):
		self.matcher = re.compile('\(.*rim.*\)|blackberry', re.IGNORECASE)

	def getParseOrder(self):
		return 2

	def doesMatch(self, ua):
		return bool(self.matcher.search(ua))

	def getOs(self):
		return 'bb'

