#! /usr/bin/python

import unittest
from agedata import ReleaseItem
from agedata import AgeData as Adata
from datetime import date
from age import *
import json

class TestAge(unittest.TestCase):

	def setUp(self):
		pass

	def testUas(self):
		age = Age('Opera/9.80 (Windows NT 5.1; U; zh-sg) Presto/2.9.181 Version/12.00')
		self.assertTrue(isinstance(age.getUa(), UaOpera))

		age = Age('Mozilla/5.0 (Windows NT 5.1) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.43 Safari/534.24')
		self.assertTrue(isinstance(age.getUa(), UaChrome))

		age = Age('Mozilla/5.0 (Windows NT 5.2; rv:2.0b13pre) Gecko/20110304 Firefox/4.0b13pre')
		self.assertTrue(isinstance(age.getUa(), UaFirefox))

		age = Age('Mozilla/5.0 (Windows; U; MSIE 9.0; WIndows NT 9.0; en-US))')
		self.assertTrue(isinstance(age.getUa(), UaMsie))

		age = Age('Mozilla/5.0 (Windows; U; Windows NT 6.1; tr-TR) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27')
		self.assertTrue(isinstance(age.getUa(), UaSafari))

		age = Age('')
		self.assertTrue(age.getUa() == None)

	def testAges(self):
		UAs = ['Opera/9.80 (Windows NT 5.1; U; zh-sg) Presto/2.9.181 Version/12.00', 
			'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.43 Safari/534.24',
			'Mozilla/5.0 (Windows NT 5.2; rv:2.0b13pre) Gecko/20110304 Firefox/4.0b13pre',
			'Mozilla/5.0 (Windows; U; MSIE 9.0; WIndows NT 9.0; en-US))',
			'Mozilla/5.0 (Windows; U; Windows NT 6.1; tr-TR) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27',
			'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1'
		]

		for u in UAs:
			age = Age(u)
			print 'UA: ', u
			print '--Age: ', age.getAge()

	def testCoverage(self):
		f = file('uas.json', 'r')
		allUas = json.loads(f.read())
		f.close()

		failures = 0
		ages = []
		for u in allUas:
			age = Age(u).getAge()
			if age:
				ages.append(age)
			else:
				failures += 1

		print '%i/%i coverage for %.2f%%' % (len(ages), len(ages)+failures, 100.*len(ages)/(failures + len(ages)))


		

if __name__ == '__main__':
	unittest.main()