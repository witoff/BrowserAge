#! /usr/bin/python

import unittest
import sys

sys.path.append('..')
from age import Age
from osparser import *

class TestOsp(unittest.TestCase):

	def setUp(self):
		pass

	def testAndroid(self):
		age = Age('Mozilla/5.0 (Linux; U; Android 4.1.1; en-gb; Galaxy Nexus Build/JRO03C) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30')
		print age.getOs()
		self.assertEqual(age.getOs(), OspAndroid().getOs())

		

if __name__ == '__main__':
	unittest.main()






