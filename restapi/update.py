import redis
import ast

rd = redis.StrictRedis(host='localhost', port=6379, db=0)

keys = rd.keys("*")

for key in keys:
	expire = rd.ttl(key)
	talk = rd.get(key)
	t = ast.literal_eval(talk)
	if 'd' not in t:
		t['d'] = '0'

	rd.getset(key, t)
	rd.expire(key, expire)
	print t
