from agedata import AgeData, ReleaseItem
#from httpagentparser as hap
from browserparser import *
from osparser import *
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

	brParsers = None
	osParsers = None

	def __init__(self, ua):
		self.ua_raw = ua
		self.ua = ua.lower()

		#Cache values
		self.age_c = None
		self.browser_c = None
		self.os_c = None

		if not Age.brParsers:
			Age.registerBrowserParsers()
		if not Age.osParsers:
			Age.registerOsParsers()

		self.brp = self.getBrParser()
		self.osp = self.getOsParser()
	
	def getBrParser(self):
		for brp in Age.brParsers:
			if brp.doesMatch(self.ua):
				return brp
		return None

	def getOsParser(self):
		for osp in Age.osParsers:
			if osp.doesMatch(self.ua):
				return osp	
		return None

	def getAge(self):
		if not self.age_c and self.brp:
			self.age_c = self.brp.getAge(self.ua)
		return self.age_c

	def getBrowser(self):
		if not self.browser_c and self.brp:
			self.browser_c = self.brp.getBrowser()
		return self.browser_c

	def getOs(self):
		if not self.os_c and self.osp:
			self.os_c = self.osp.getOs()
		return self.os_c

	@staticmethod
	def registerBrowserParsers():
		Age.brParsers = [c() for c in globals().values() if BrowserParser in getattr(c, '__mro__', [])]
		Age.brParsers.sort(key=lambda p: p.getParseOrder())

	@staticmethod
	def registerOsParsers():
		Age.osParsers = [c() for c in globals().values() if OsParser in getattr(c, '__mro__', [])]
		Age.osParsers.sort(key=lambda p: p.getParseOrder())
       
	def getUa(self):
		return self.brp

