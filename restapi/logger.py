from datetime import date, time, datetime

class Logger:
	def __init__(self, logPath):
		self.logPath = logPath

	def writeLog(self, log):
		f = open(self.logPath, "a")
		f.write("\n-----" + datetime.now().strftime('%y-%m-%d %H:%M:%S')+ "--------------------\n")
		f.write(log + "\n")
		f.close()
