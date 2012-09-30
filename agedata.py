import json
from datetime import date, datetime, timedelta
from os import path

class ReleaseItem(object):
	""" Hold and compare date elements """

	def __init__(self, version, releaseDate = None):
		
		if isinstance(version, list):
			self.ver = version
		else:
			self.ver = [ version ]

		#Coerce to an int version
		for i in range(len(self.ver)):
			if isinstance(self.ver[i], basestring):
				intVer = int('0'+ ''.join([s for s in self.ver[i] if s.isdigit()]))
				self.ver[i] = intVer

		self.releaseDate = releaseDate

	@staticmethod
	def has_non_zero_els(arr):
		for e in arr:
			if e!=0:
				return True
			"""
			if e.isalnum() and not e.isdigit():
				#has a letter
				return True
			if e.isdigit() and int(e)>0:
				return True
			"""
		return False

	def extendVersion(self, length):
		delta = length-len(self.ver)
		self.ver.extend( [0]*delta )

	def compare(self, other):
		if isinstance(other, list):
			other = ReleaseItem(other)

		if self.ver == other.ver:
			return 0

		for i in range(len(self.ver)):

			if i == len(other.ver):
				if ReleaseItem.has_non_zero_els(self.ver[i:]):
					return 1
				return 0

			
			"""
			#handle alphas w/ 0 padding
			ls = len(self.ver[i])
			lo = len(other.ver[i])
			if ls > lo:
				other.ver[i] = '0'*(ls-lo) + other.ver[i]
			elif lo > ls:
				self.ver[i] = '0'*(lo-ls) + self.ver[i]
			"""

			if self.ver[i] > other.ver[i]:
				return 1
			if self.ver[i] < other.ver[i]:
				return -1
		
		if len(self.ver) < len(other.ver) and \
			ReleaseItem.has_non_zero_els(other.ver[len(self.ver):]):
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

	def __init__(self, filename, propLimit=2):
		self.propLimit=propLimit
		localPath = path.dirname(path.realpath(__file__))
		self.filename = path.join(localPath, 'data', filename)
		self.versionElements = 0
		self.releases = []
		self.deltas = None
		self.deltasAvg = None

		# Load
		self.loadDates()
		self.loadDeltas()

	def loadDates(self):
		f = file(self.filename, 'r')
		fullDict = json.loads(f.read())
		releaseData = fullDict.values()[0]

		for k, v in releaseData.iteritems():
			dateEls = v.split('-')
			d = date(int(dateEls[0]), int(dateEls[1]), int(dateEls[2]))
			self.releases.append(ReleaseItem(k.split('.'), d))

		self.normalizeVersionLengths()

		#make all releases the same length
		self.releases.sort()

	def normalizeVersionLengths(self):
		#Normalize length of all versions with added zeros
		longest = 0
		for ri in self.releases:
			longest = max(longest, len(ri.ver))
		for ri in self.releases:
			ri.extendVersion(longest)
		self.versionElements = longest



	def loadDeltas(self):
		deltas = {}
		for i in xrange(len(self.releases)):
			if i==0:
				continue
			rCur = self.releases[i]
			rLast = self.releases[i-1]

			#find the current version index that has changed
			changedIndex = -1
			for j in range(len(rCur.ver)):
				vC = rCur.ver[j]
				vL = rLast.ver[j]
				if vC != vL:
					changedIndex = j
					break
			if changedIndex<0:
				continue
			
			#find when this version index was last incremented and set rLast to that last delta
			#print 'CHANGE: ', rCur.ver, rLast.ver
			for j in xrange(i-1,-1,-1):
				#print 'index: %i j: %s, i:  %s' % (changedIndex, self.releases[j].ver[changedIndex],  self.releases[i-1].ver[changedIndex])
				if self.releases[j].ver[changedIndex] == self.releases[i-1].ver[changedIndex]:
					rLast = self.releases[j]
				else:
					break



			if deltas.get(changedIndex):
				deltas[changedIndex].append({'date': rCur.releaseDate, 'delta': rCur.releaseDate - rLast.releaseDate})
			else:
				deltas[changedIndex] = [{'date': rCur.releaseDate, 'delta': rCur.releaseDate - rLast.releaseDate}]


			#Loop through all prior elements.. what is the highest digit that changed?
		self.deltas = deltas
		
		self.deltasAvg = []
		for i in range(self.versionElements):
			if self.deltas.get(i):
				days = [d['delta'].days for d in self.deltas.get(i)]
				self.deltasAvg.append( timedelta(sum(days)/float(len(days))) )
			else:
				self.deltasAvg.append(timedelta(0) if not self.deltasAvg else self.deltasAvg[i-1]*0)
		#print self.deltasAvg		


	def getDate(self, releaseItem):
		#TODO: Better fitting b/w release dates
		if isinstance(releaseItem, list):
			releaseItem = ReleaseItem(releaseItem)
		#Normalize the new item's length
		releaseItem.extendVersion(self.versionElements)

		for i in range(len(self.releases)):
			ri = self.releases[i]

			if ri == releaseItem:
				return ri.releaseDate
			elif ri > releaseItem:
				return self.propagateDate(self.releases[max(i-1,0)], releaseItem)
		return self.propagateDate(self.releases[-1], releaseItem)


	
	def propagateDate(self, reference, current):
		if reference==current:
			return reference.releaseDate

		for i in range(self.versionElements):
			if reference.ver[i]!=current.ver[i]:
				totalTd = self.deltasAvg[i] * min(self.propLimit, (current.ver[i] - reference.ver[i]))
				for j in range(i+1, len(self.deltasAvg)):
					pass
					totalTd += self.deltasAvg[j] * min(self.propLimit, current.ver[j])
				return min(datetime.today().date(), reference.releaseDate + totalTd)

		i = self.versionElements-1
		nextDate = reference.releaseDate + self.deltasAvg[i] * (current.ver[i] - reference.ver[i])
		min(datetime.today().date(), nextDate)

