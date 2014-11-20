import redis
import ast

redis = redis.StrictRedis(host='localhost', port=6379, db=0)

key = "28499950-7085-11e4-9890-7071bcbc887a"
talk = ast.literal_eval(redis.get(key))

talk['t'] = talk['t'].replace('"', "'")

exp = redis.ttl(key)

redis.delete(key)

redis.setnx(key, talk)


