import redis
import ast

redis = redis.StrictRedis(host='localhost', port=6379, db=0)

talk = ast.literal_eval(redis.get("28499950-7085-11e4-9890-7071bcbc887a"))

talk['t'] = talk['t'].replace('"', "'")

print talk['t']


