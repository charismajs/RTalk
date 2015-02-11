import redis
import uuid
import ast
from datetime import datetime, date, time

# 14 Days
#EXPIRE = 60 * 60 * 24 * 14
EXPIRE = 60 * 60 * 24

class RedisDataSource:
	def __init__(self):
		self.redis = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
		
	def getTalks(self):
		keys = self.redis.keys("*")
		
		return self.redis.mget(keys)

	def setTalk(self, talkString):
		key = str(uuid.uuid1())

		talkStr = talkString.replace('\\', '\\\\').replace('"', '\\"')

		talk = {'k':key,'t':talkStr,'wt':datetime.now().strftime('%y-%m-%d %H:%M:%S'),'l':'0','d':'0'}

		while self.redis.setnx(key, talk) == False:
			key = str(uuid.uuid1())

			talk['k'] = key

		remainDay = 6 - date.today().weekday() + 6
		self.redis.expire(key, EXPIRE * remainDay)

	def setLike(self, key):
		if self.redis.exists(key) == True:
			exp = self.redis.ttl(key)
			talk = ast.literal_eval(self.redis.get(key))
			talk['l'] = int(talk['l']) + 1
			self.redis.getset(key, talk)
			self.redis.expire(key, exp)
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
