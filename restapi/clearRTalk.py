from redisDatasource import RedisDataSource
from logger import Logger
import os

rd = RedisDataSource()

rd.deleteAll()

logger = Logger(os.getcwd() + "/clearTalks.log")
logger.writeLog("Clear Talks")
