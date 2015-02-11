from flask import Flask, jsonify, render_template, request, send_file, abort 
import sys
from rtalk import RTalk, RTalkList
from redisDatasource import RedisDataSource
from logger import Logger

app = Flask(__name__)
rd = RedisDataSource()
logger = Logger("/Users/hoyoonlee/Documents/workspace/RTalk/restapi/webRTalk.log")

def makeJson(arrayName, talks):
	jsonTalks = []

	for talk in talks:
		jsonTalks.append(talk.toString())

	return '"' + arrayName + '":[' + ",".join(jsonTalks) + "]"

def makeJsonResponse(resp):
	return Response(resp, mimetype='application/json')

@app.route('/list/<int:topn>/<int:listcount>', methods=['GET'])
def list(topn, listcount):
	try:
		talks = rd.getTalks()

		if len(talks) == 0 :
			return jsonify({'result':'error','reason':'no keys'})

		rtalks = []

		for talk in talks:
			rtalks.append(RTalk(talk))

		rtalkList = RTalkList(rtalks)

		topTalks = rtalkList.getTopN(topn)
		genTalks = rtalkList.getList(listcount)

		return "{" + makeJson("topn", topTalks) + "," + makeJson("list", genTalks) + "}"
		# return "{}"
	except Exception as e:
		logger.writeLog("error [def list] : %s" % e)
		abort(500)

@app.route('/write', methods=['POST'])
def write():
	try:

		if not request.json:
			abort(400)

		if 'talk' in request.json and type(request.json['talk']) != unicode:
			abort(400)

		rtalk = request.json['talk']

		rtalk = rtalk.strip()

		if len(rtalk) == 0:
			abort(400)
			return jsonify({'result':'error'})
		else:
			rd.setTalk(rtalk)
			return jsonify({'result':'ok'})
	except Exception as e:
		logger.writeLog("error [def write] : %s" % e)
		abort(500)

@app.route('/like/<key>', methods=['GET'])
def like(key):
	try:
		rd.setLike(key)
		return jsonify({'result':'ok'})
	except Exception as e:
		logger.writeLog("error [def like] : %s" % e)
		abort(500)

@app.route('/dislike/<key>', methods=['GET'])
def dislike(key):
	try:
		rd.setDislike(key)
		return jsonify({'result':'ok'})
	except Exception as e:
		logger.writeLog("error [def like] : %s" % e)
		abort(500)

if __name__ == '__main__':
	#app.debug = True

	hostIp = "0.0.0.0"

	if sys.argv[1] == "production":
		hostIp = "127.0.0.1"

	app.run(host=hostIp, port=5001)
