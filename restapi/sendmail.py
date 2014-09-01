import smtplib
import redis
from rtalk import RTalk, RTalkList
from datetime import datetime, date, time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

DIR="/home/RTalk/restapi/"

HOST = "122.199.153.32"
PORT = 25
FROM = "ubcarernd@gmail.com"
SUBJECT = "R&D Talk TOP 3"
TOPCOUNT = 3

rd = redis.StrictRedis(host='localhost',port=6379,db=0)

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

		writeLog(emailtext)
	except Exception as e:
		print e		

def gettalk():
	try:
		keys = rd.keys("*")

		if len(keys) == 0 :
			return jsonify({'result':'error','reason':'no keys'})

		talks = rd.mget(keys)

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

def writeLog(msg):
	f = open(DIR + "sendmail.log", 'a')

	f.write(datetime.now().strftime('%y-%m-%d %H:%M:%S')+ "--------------------------------------------------------------------------------------------------------\n")	
	f.write(msg + "\n")

	f.close()

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
		#rd.delete(talk.key)	
else:
	writeLog("Send Mail : None")
