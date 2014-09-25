import redis
import uuid
import ast
from datetime import datetime, date, time

# 14 Days
EXPIRE = 60 * 60 * 24 * 14

class RedisDataSource:
	def __init__(self):
		self.redis = redis.StrictRedis(host='localhost', port=6379, db=0)
		
	def getTalks(self):
		keys = self.redis.keys("*")
		
		return self.redis.mget(keys)

	def setTalk(self, talkString):
		key = str(uuid.uuid1())

		if self.redis.exists(key) == True:
			return self.setTalk(talkString)

		talk = {'k':key,'t':talkString,'wt':datetime.now().strftime('%y-%m-%d %H:%M:%S'),'l':'0','d':'0'}

		self.redis.setex(key, EXPIRE, talk)

	def setLike(self, key):
		if self.redis.exists(key) == True:
			expire = self.redis.ttl(key)
			talk = ast.literal_eval(self.redis.get(key))
			talk['l'] = int(talk['l']) + 1
			self.redis.getset(key, talk)
			self.redis.expire(key, expire)
		#return ast.literal_eval(self.redis.get(key))

	def setDislike(self, key):
		if self.redis.exists(key) == True:
			expire = self.redis.ttl(key)
			talk = ast.literal_eval(self.redis.get(key))
			talk['d'] = int(talk['d']) + 1
			self.redis.getset(key, talk)
			self.redis.expire(key, expire)
		
	def deleteTalk(self, key):
		if self.redis.exists(key) == True:
			self.redis.delete(key)

	def deleteAll(self):
		keys = self.redis.keys("*")

		for key in keys:
			self.redis.delete(key)
