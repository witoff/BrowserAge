#! /usr/bin/python

import unittest
from agedata import ReleaseItem
from agedata import AgeData as Adata
from datetime import date
from age import *
from os import path
from browserparser import *
import json

class TestAge(unittest.TestCase):

	def setUp(self):
		pass

	def testUas(self):
		age = Age('Opera/9.80 (Windows NT 5.1; U; zh-sg) Presto/2.9.181 Version/12.00')
		self.assertTrue(isinstance(age.getUa(), BrpOpera))

		age = Age('Mozilla/5.0 (Windows NT 5.1) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.43 Safari/534.24')
		self.assertTrue(isinstance(age.getUa(), BrpChrome))

		age = Age('Mozilla/5.0 (Windows NT 5.2; rv:2.0b13pre) Gecko/20110304 Firefox/4.0b13pre')
		self.assertTrue(isinstance(age.getUa(), BrpFirefox))

		age = Age('Mozilla/5.0 (Windows; U; MSIE 9.0; WIndows NT 9.0; en-US))')
		self.assertTrue(isinstance(age.getUa(), BrpMsie))

		age = Age('Mozilla/5.0 (Windows; U; Windows NT 6.1; tr-TR) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27')
		self.assertTrue(isinstance(age.getUa(), BrpSafari))

		age = Age('')
		self.assertTrue(age.getUa() == None)

	def testAges(self):
		UAs = ['Opera/9.80 (Windows NT 5.1; U; zh-sg) Presto/2.9.181 Version/12.00', 
			'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.43 Safari/534.24',
			'Mozilla/5.0 (Windows NT 5.2; rv:2.0b13pre) Gecko/20110304 Firefox/4.0b13pre',
			'Mozilla/5.0 (Windows; U; MSIE 9.0; WIndows NT 9.0; en-US))',
			'Mozilla/5.0 (Windows; U; Windows NT 6.1; tr-TR) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27',
			'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1',
			'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1229.79 Safari/537.4',
			'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/536.26.14 (KHTML, like Gecko) Version/6.0.1 Safari/536.26.14',
			'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.46 Safari/536.5'
		]

		for u in UAs:
			print 'UA: ', u
			age = Age(u)
			num = age.getAge()
			brow = age.getBrowser()
			os = age.getOs()

			print '--Age: ', num
			print '--Browser: ', brow
			print '--Os: ', os

	def testCoverage(self):
		f = file(path.join('data', 'uas.json'), 'r')
		allUas = json.loads(f.read())
		f.close()

		ages = []
		age_failures = 0

		oss = []
		os_failures = 0
		for u in allUas:
			a = Age(u)
			age = a.getAge()
			if age:
				ages.append(age)
			else:
				age_failures += 1

			os = a.getOs()
			if os:
				oss.append(os)
			else:
				os_failures += 1


		print 'Age Coverage: %i/%i coverage for %.2f%%' % (len(ages), len(ages)+age_failures, 100.*len(ages)/(age_failures + len(ages)))
		print 'OS Coverage: %i/%i coverage for %.2f%%' % (len(oss), len(oss)+os_failures, 100.*len(oss)/(os_failures + len(oss)))


		

if __name__ == '__main__':
	unittest.main()
