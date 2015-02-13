from pymongo import MongoClient

class RTalkMongo:
	def __init__(self):
		self.mongoClient = MongoClient()
		self.mongoDb = self.mongoClient.weeklyRTalks
		self.rtalks = self.mongoDb.rtalks

	def write(self, talkString):
		rtalkMongoId = self.rtalks.insert(talkString)
		print rtalkMongoId

	def topRTalkCollection(self):
		topRTalks = {}
		subRTalks = []

		for rtalk in self.rtalks.find():
			if rtalk['sd'] in topRTalks:
				topRTalks[rtalk['sd']].append(rtalk['t'])
			else:
				subRTalks.append(rtalk['t'])
				topRTalks[rtalk['sd']] = subRTalks

		
