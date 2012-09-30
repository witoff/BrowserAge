#! /usr/bin/python

import unittest
import sys

sys.path.append('..')
from agedata import ReleaseItem
from agedata import AgeData as Adata
from datetime import date, timedelta

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


class TestAgeData(unittest.TestCase):

	def setUp(self):
		#self.data = AgeData(['arst'])
		#self.ad.load()
		pass
	
	def testMatch(self):
		ad = Adata('age-chrome.json')

		self.assertTrue(ad.getDate(['20']) >= \
		 	ad.getDate(['12']) >= \
			ad.getDate(['10']) >= \
			ad.getDate(['5']) >= \
			ad.getDate(['1']))

	def testNormalize(self):
		ad = Adata('age-msie.json')
		for ri in ad.releases:
			self.assertEqual(len(ri.ver), len(ad.releases[0].ver))

	def test0thDelta(self):
		ad = Adata('age-msie.json')

		ad.releases = []
		ad.releases.append(ReleaseItem(['1', '0', '0'], date(2000, 1, 1)))
		ad.releases.append(ReleaseItem(['2', '0', '0'], date(2000, 1, 2)))
		ad.releases.append(ReleaseItem(['3', '0', '0'], date(2000, 1, 3)))
		ad.loadDeltas()
		self.assertEqual(len(ad.deltas.viewkeys()), 1)
		self.assertTrue(ad.deltas.get(0))

		for d in ad.deltas[0]:
			self.assertEqual(d['delta'].days, 1)

	def test0thDelta2(self):
		ad = Adata('age-msie.json')

		ad.releases = []
		ad.releases.append(ReleaseItem(['1', '9', '0'], date(2000, 1, 1)))
		ad.releases.append(ReleaseItem(['2', '0', '0'], date(2000, 1, 2)))
		ad.loadDeltas()
		self.assertEqual(len(ad.deltas.viewkeys()), 1)
		self.assertTrue(ad.deltas.get(0))

		for d in ad.deltas[0]:
			self.assertEqual(d['delta'].days, 1)
	

	def test0thDeltaWithSteps(self):
		ad = Adata('age-msie.json')

		# CREATE
		ad.releases = []
		ad.releases.append(ReleaseItem(['0', '9', '0'], date(2000, 1, 1)))
		ad.releases.append(ReleaseItem(['1', '1', '0'], date(2000, 1, 3)))
		ad.releases.append(ReleaseItem(['1', '2', '0'], date(2000, 1, 4)))
		ad.releases.append(ReleaseItem(['2'], date(2000, 1, 5)))
		ad.releases.sort()
		ad.normalizeVersionLengths()
		ad.loadDeltas()

		# VALIDATE LOADING
		self.assertEqual(len(ad.deltas.viewkeys()), 2)
		self.assertTrue(ad.deltas.get(0))
		self.assertTrue(ad.deltas.get(1))

		for d in ad.deltas[0]:
			self.assertEqual(d['delta'].days, 2)
		self.assertEqual(ad.deltasAvg[0], timedelta(2))

		# VALIDATE PROPAGATION
		self.assertEqual(ad.getDate([3,0,0]), date(2000,1,7))
		print ad.getDate([3,0,0])
		print ad.getDate([4,0,0])
		print ad.getDate([3,5,0])
		print ad.getDate([3,0,1])
		print ad.getDate([3,0,0,1])
		print ad.getDate([2,5,0,1])

		#TODO: Test intermediate values


if __name__ == '__main__':
	unittest.main()


