import sys
#from email.mime.multipart import MIMEMultipart
#from email.mime.text import MIMEText
#from email import Utils
from logger import Logger
#import smtplib


import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
from email import Utils
from email.header import Header
import os

DIR = "/home/RTalk/restapi/"

HOST = "122.199.153.32"
PORT = 25

logger = Logger(DIR + "sendmail.log")

def sendmail(sender, receivers, subject, plaintext, htmltext):
	try:
		toList = ",".join(receivers)
		email = MIMEMultipart('alternative')
		email['Subject'] = Header(s=subject, charset="utf-8") 
		email['From'] = sender
		email['To'] = toList
		email["Date"] = Utils.formatdate(localtime=1)

		email.attach(MIMEText(plaintext, 'plain', 'utf-8'))
		email.attach(MIMEText(htmltext, 'html', 'utf-8'))

		server = smtplib.SMTP(HOST, PORT)

		emailtext = email.as_string()
		server.sendmail(sender, receivers, emailtext)
		server.close()

		logger.writeLog(emailtext)
	except Exception as e:
		logger.writeLog(str(e))


