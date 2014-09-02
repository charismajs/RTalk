from flask import Flask, jsonify, render_template, request, send_file, abort
import sys
from rtalk import RTalk, RTalkList
from redisDatasource import RedisDataSource

app = Flask(__name__)
rd = RedisDataSource()

def makeJson(arrayName, talks):
	jsonTalks = []

	for talk in talks:
		jsonTalks.append(talk.toString())

	return '"' + arrayName + '":[' + ",".join(jsonTalks) + "]"

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
	except Exception as e:
		return jsonify({'result':'error', 'reason':e })

@app.route('/write', methods=['POST'])
def write():
	try:
		if not request.json:
			abort(400)

		if 'talk' in request.json and type(request.json['talk']) != unicode:
			abort(404)

		rtalk = request.json['talk']

		return jsonify(rd.setTalk(rtalk))
	except Exception as e:
		return jsonify({'result':'error', 'reason':e })

@app.route('/like/<key>', methods=['GET'])
def like(key):
	try:
		return jsonify(rd.setLike(key))
	except Exception as e:
		return jsonify({'result':'error', 'reason':e })	

if __name__ == '__main__':
	#app.debug = True
	#app.run(host=sys.argv[1],port=5001)
	app.run(host="127.0.0.1",port=5001)
