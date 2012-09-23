import json
from datetime import date, datetime

class ReleaseItem(object):
	""" Hold and compare date elements """

	def __init__(self, version, releaseDate = None):
		
		if isinstance(version, list):
			self.ver = version
		else:
			self.ver = [ version ]

		self.releaseDate = releaseDate

	@staticmethod
	def has_non_zero_els(arr):
		for e in arr:
			if e.isalnum() and not e.isdigit():
				#has a letter
				return True
			if e.isdigit() and int(e)>0:
				return True
		return False

	def compare(self, other):
		if isinstance(other, list):
			other = ReleaseItem(other)

		if self.ver == other.ver:
			return 0

		for i in range(len(self.ver)):

			if i >= len(other.ver):
				if ReleaseItem.has_non_zero_els(self.ver[i]):
					return 1
				return 0

			
			#handle alphas w/ 0 padding
			ls = len(self.ver[i])
			lo = len(other.ver[i])
			if ls > lo:
				other.ver[i] = '0'*(ls-lo) + other.ver[i]
			elif lo > ls:
				self.ver[i] = '0'*(lo-ls) + self.ver[i]

			if self.ver[i] > other.ver[i]:
				return 1
			if self.ver[i] < other.ver[i]:
				return -1
		
		if ReleaseItem.has_non_zero_els(other.ver[len(self.ver)]):
			return -1
		return 0

	def __gt__(self, other):
		return self.compare(other) == 1

	def __ge__(self, other):
		return self.compare(other) in [1,0]

	def __lt__(self, other):
		return self.compare(other) == -1

	def __le__(self, other):
		return self.compare(other) in [-1, 0]

	def __eq__(self, other):
		return self.compare(other) == 0



class AgeData(object):
	""" Access and Fit to Age Datasets """

	def __init__(self, filename):
		self.filename = filename
		self.releases = []

	def load(self):
		f = file(self.filename, 'r')
		fullDict = json.loads(f.read())
		releaseData = fullDict.values()[0]

		leases = []
		for k, v in releaseData.iteritems():
			dateEls = v.split('-')
			d = date(int(dateEls[0]), int(dateEls[1]), int(dateEls[2]))
			self.releases.append(ReleaseItem(k.split('.'), d))
		self.releases.sort()


	def getDate(self, releaseItem):
		#TODO: Better fitting b/w release dates
		if isinstance(releaseItem, list):
			releaseItem = ReleaseItem(releaseItem)

		for i in range(len(self.releases)):
			ri = self.releases[i]

			if ri >= releaseItem:
				return ri.releaseDate
		print 'NO MATCHES'
		return datetime.now().date()


