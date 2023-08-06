import os
import time
import nextapm.lib.logger as logger
from .constants import NEXTAPM_LICENSE_KEY, NEXTAPM_PROJECT_ID

try:
    from collections.abc import Callable
except ImportError:
    from collections import Callable

def currentMillis():
    return int(round(time.time() * 1000))

def isCallable(fn):
    return isinstance(fn, Callable)

def validateConfig():
    licenseKey = os.getenv(NEXTAPM_LICENSE_KEY, '')
    if not licenseKey:
        logger.error('Configure license key in NEXTAPM_LICENSE_KEY environment variable')
        return False
    
    projectId = os.getenv(NEXTAPM_PROJECT_ID, '') 
    if not projectId:
        logger.error('Configure project id in NEXTAPM_PROJECT_ID environment variable')
        return False

    return True
