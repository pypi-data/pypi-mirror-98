from nextapm.lib.util import currentMillis
from nextapm.lib.data.transport import sendMetrics
import nextapm.lib.logger as logger

class Transaction:

    def __init__(self, info={}):
        self.url = info.get('path', '')
        self.method = info.get('command', '')
        self.startTime = currentMillis()
        self.endTime = None
        self.rt = 0
        self.completed = False
        self.status = 200
        self.exceptionsInfo = {}

    def end(self):
        try:
            self.endTime = currentMillis()
            self.rt = self.endTime - self.startTime
            self.completed = True
            sendMetrics(self)
        except Exception as e:
            logger.error('[Transaction][end]', e)

    def getAsJson(self):
        return {
          'url': self.url,
          'method': self.method,
          'start': self.startTime,
          'status': self.status,
          'rt': self.rt,
        }

    def isCompleted(self):
        return self.completed

    def setUrl(self, url):
        if type(url) is str:
            self.url = url

    def setMethod(self, method):
        if type(method) is str:
            self.method = method

    def setStatus(self, code):
        if type(code) is int:
            self.status = code
