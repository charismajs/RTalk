import smtplib
from rtalk import RTalk, RTalkList
from datetime import datetime, date, time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from redisDatasource import RedisDataSource
from logger import Logger
import os

DIR = os.getcwd() + "/"

HOST = "122.199.153.32"
PORT = 25
FROM = "RDPart@ubcare.co.kr"
SUBJECT = "Weekly R&D Talk TOP 3"
TOPCOUNT = 3

rd = RedisDataSource() 
logger = Logger(DIR + "sendmail.log")

def sendmail(receivers, topTalks):
	try:
		toList = ",".join(receivers)
		email = MIMEMultipart('alternative')
		email['Subject'] = SUBJECT
		email['From'] = FROM
		email['To'] = toList 

		plaintext = makeEmail(makeMessage(topTalks, "%s, %s, %s"), "%s")
		htmltext = makeEmail(makeMessage(topTalks, getTemplate("contenttemplate")), getTemplate("emailtemplate"))

		email.attach(MIMEText(plaintext, 'plain'))
		email.attach(MIMEText(htmltext, 'html'))
	
		server = smtplib.SMTP(HOST, PORT)
		#server.ehlo()
		#server.starttls()
		#server.login(USERID, PASSWD)
		
		emailtext = email.as_string()
		server.sendmail(FROM, toList, emailtext)
		server.close()

		logger.writeLog(emailtext)
	except Exception as e:
		print e		

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
		print e		

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
		print e

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
	receivers.append(line.rstrip('\n'))

emaillist.close()

topTalks = gettalk()

if len(topTalks) > 0 and len(receivers) > 0:
	sendmail(receivers, topTalks)

	for talk in topTalks:
		print "Delete Talk : " + talk.key
		rd.deleteTalk(talk.key)	
else:
	logger.writeLog("Send Mail : None")
