import smtplib
from rtalk import RTalk, RTalkList
from datetime import datetime, date, time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from redisDatasource import RedisDataSource
from logger import Logger
import mailsender
import datetime

DIR = "/home/RTalk/restapi/"

FROM = "RDPart@ubware.com"
SUBJECT = "Weekly R&D Talk TOP 3"
TOPCOUNT = 3

rd = RedisDataSource() 
logger = Logger(DIR + "sendmail.log")
holidayList = []

def readHoliday():
	holidayFile = open("/home/RTalk/restapi/holiday.lst", "r")

	while True:
		holiday = holidayFile.readline().strip()
		if not holiday:
			break
		holidayList.append(datetime.datetime.strptime(holiday, "%Y-%m-%d").date())

	holidayFile.close()

def isHoliday(date):
	return date in holidayList

def sendmail(receivers, topTalks):
	plaintext = makeEmail(makeMessage(topTalks, "{0}, like {2}, dislike {3}, {1}"), "%s")
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
			t = t.replace("{3}", str(talk.dislike))
			talkmessages.append(t)

		return u"\n".join(talkmessages).encode('utf-8')
	except Exception as e:
		logger.writeLog(str(e))

def makeEmail(msg, template):
	return template.replace('%s', msg)

def getTemplate(filename):
	with open(DIR + filename, "r") as f:
		return f.read()

def canSendmail():
	today = datetime.datetime.today().weekday()

	sendmailDayOfWeek = 4

	if today > sendmailDayOfWeek:
		return False

	intervalDay = sendmailDayOfWeek - today

	sendmailDate = date.today() + datetime.timedelta(days=intervalDay)

	readHoliday()

	while True:
		if isHoliday(sendmailDate):
			sendmailDate = sendmailDate - datetime.timedelta(days=1)
			continue

		break

	dow = sendmailDate.weekday()

	return today == dow

if canSendmail() == False:
	print "Not Today"
	exit()

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
		#rd.deleteTalk(talk.key)	
else:
	logger.writeLog("Send Mail : None")
