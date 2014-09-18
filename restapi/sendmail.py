import smtplib
from rtalk import RTalk, RTalkList
from datetime import datetime, date, time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from redisDatasource import RedisDataSource
from logger import Logger
import mailsender

DIR = "/home/RTalk/restapi/"

#FROM = "jeonyoungmin@ubware.com"
FROM = "RDPart@ubware.com"
#FROM = "ubcarernd@gmail.com"
SUBJECT = "Weekly R&D Talk TOP 3"
TOPCOUNT = 3

rd = RedisDataSource() 
logger = Logger(DIR + "sendmail.log")

def sendmail(receivers, topTalks):
	plaintext = makeEmail(makeMessage(topTalks, "{0}, like {2}, {1}"), "%s")
	htmltext = makeEmail(makeMessage(topTalks, getTemplate("contenttemplate")), getTemplate("emailtemplate"))

	mailsender.sendmail(FROM, receivers, SUBJECT, plaintext, htmltext)

def gettalk():
	try:
		talks = rd.getTalks()

		if len(talks) == 0:
			return jsonify({'result':'error','reason':'no keys'})

		rtalks = []

		for talk in talks:
			rtalks.append(RTalk(talk))

		rtalkList = RTalkList(rtalks)

		return rtalkList.getTopN(TOPCOUNT)

	except Exception as e:
		logger.writeLog(str(e))

def makeMessage(talks, template):
	try:
		if len(talks) == 0:
			return None

		talkmessages = []

		for talk in talks:
			t = template.replace("{0}", talk.talk)
			t = t.replace("{1}", talk.writetime.strftime('%y-%m-%d %H:%M'))
			t = t.replace("{2}", str(talk.like))
			talkmessages.append(t)

		return u"\n".join(talkmessages).encode('utf-8')
	except Exception as e:
		logger.writeLog(str(e))

def makeEmail(msg, template):
	return template.replace('%s', msg)

def getTemplate(filename):
	with open(DIR + filename, "r") as f:
		return f.read()

receivers = []

emaillist = open(DIR + "emaillist", "r")

while True:
	line = emaillist.readline()
	if not line:
		break
	receivers.append(line.rstrip('\n') + "@ubware.com")

emaillist.close()

topTalks = gettalk()

if len(topTalks) > 0 and len(receivers) > 0:
	sendmail(receivers, topTalks)

	for talk in topTalks:
		print "Delete Talk : " + talk.key
		rd.deleteTalk(talk.key)	
else:
	logger.writeLog("Send Mail : None")
