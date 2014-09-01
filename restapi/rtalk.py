from datetime import datetime, date, time
from itertools import ifilter
import ast

class RTalk:
    def __init__(self, talk):
		self.rtalk = ast.literal_eval(talk)
		self.talk = self.rtalk['t']
		self.writetime = datetime.strptime(self.rtalk['wt'], '%y-%m-%d %H:%M:%S')
		self.like = int(self.rtalk['l'])
		self.key = self.rtalk['k']

    def __repr__(self):
        return repr((self.key, self.talk, self.writetime, self.like))

    def toString(self):
        talk = '{"k":"' + self.key + '","t":"' + self.talk + '","wt":"' + self.writetime.strftime('%y-%m-%d %H:%M:%S') + '","l":"' + str(self.like) + '"}'
        return talk


class RTalkList:
	def __init__(self, rtalks):
		self.topTalks = []
		self.rtalks = rtalks
		#self.rtalks = sorted(self.rtalks, key=lambda talk:talk.writetime, reverse=True)
		#self.rtalks = sorted(self.rtalks, key=lambda talk:talk.like, reverse=True)
		self.topCount = 0

	def getTopN(self, topCount):
		self.topCount = topCount

		self.topTalks = ifilter(lambda talk: talk.like > 0, self.rtalks)
		self.topTalks = sorted(self.topTalks, key=lambda talk:talk.writetime, reverse=True)
		self.topTalks = sorted(self.topTalks, key=lambda talk:talk.like, reverse=True)
		
		if len(self.topTalks) >= self.topCount:
			self.topTalks = self.topTalks[:self.topCount]

		return self.topTalks

	def getList(self, count):
		listCount = 0

		topTalkKeys = []

		for talk in self.topTalks:
			topTalkKeys.append(talk.key)

		genList = ifilter(lambda talk:talk.key not in topTalkKeys, self.rtalks)
		genList = sorted(genList, key=lambda talk:talk.writetime, reverse=True)

		if len(genList) >= count and count > 0:
			genList = genList[:count]

		return genList
