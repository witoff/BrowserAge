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
		if self.brp:
			return self.brp.getAge(self.ua)
		return None

	def getBrowser(self):
		if self.brp:
			return self.brp.getBrowser()
		return None

	def getOs(self):
		if self.osp:
			return self.osp.getOs()
		return None

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

