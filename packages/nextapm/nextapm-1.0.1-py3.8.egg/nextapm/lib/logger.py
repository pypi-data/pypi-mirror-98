import os

LEVELS = ['DEBUG', 'INFO', 'WARN', 'ERROR']

levelStr = os.getenv('NEXTAPM_LOG_LEVEL', 3)
configuredLevel = int(levelStr)

def log(level, msg, obj):
    if configuredLevel <= level:
        level = LEVELS[configuredLevel]
        logMsg = '[NextApm][Agent]['+level+'] ' + str(msg)
        print(logMsg, obj)


def debug(msg, data={}):
    log(0, msg, data)

def info(msg, data={}):
    log(1, msg, data)

def warn(msg, data={}):
    log(2, msg, data)

def error(msg, e=None):
    log(3, msg, e)
