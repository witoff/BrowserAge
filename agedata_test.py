#! /usr/bin/python

import unittest
from agedata import ReleaseItem
from agedata import AgeData as Adata
from datetime import date

class TestReleaseItem(unittest.TestCase):

	def setUp(self):
		self.r1 = ReleaseItem(['1','2', '3'], date(2009, 3, 1))
		self.r2 = ReleaseItem(['12', '00'])

	def testEq(self):
		self.assertTrue(self.r1 == ReleaseItem(['1','2','3']))
		self.assertTrue(self.r1 == ReleaseItem(['1','2','3', '0']))
		self.assertTrue(self.r2 == ReleaseItem(['12','00']))
		self.assertFalse(self.r1 == ReleaseItem(['12','00']))
	
	def testLt(self):
		self.assertTrue(self.r1 < ReleaseItem(['2','2','3']))
		self.assertTrue(self.r1 < ReleaseItem(['1','3','3']))
		self.assertTrue(self.r1 < ReleaseItem(['1','2','3', '1']))
	
	def testGt(self):
		self.assertTrue(self.r1 > ReleaseItem(['1','2']))
		self.assertTrue(self.r1 > ReleaseItem(['1','2','2']))
		self.assertTrue(self.r1 > ReleaseItem(['1']))
		self.assertTrue(self.r1 > ReleaseItem(['1']))


class AgeData(unittest.TestCase):

	def setUp(self):
		#self.data = AgeData(['arst'])
		#self.ad.load()
		pass

	def testMatch(self):
		self.ad = Adata('age-chrome.json')
		self.ad.load()

		self.assertTrue(self.ad.getDate(['20']) >= \
		 	self.ad.getDate(['12']) >= \
			self.ad.getDate(['10']) >= \
			self.ad.getDate(['5']) >= \
			self.ad.getDate(['1']))


if __name__ == '__main__':
	unittest.main()