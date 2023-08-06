import os
import unittest
from .util import isCallable, currentMillis, validateConfig
from .constants import NEXTAPM_LICENSE_KEY, NEXTAPM_PROJECT_ID

def clearEnv():
    os.environ[NEXTAPM_LICENSE_KEY] = ''
    os.environ[NEXTAPM_PROJECT_ID] = ''

class UtilTest(unittest.TestCase):

    def test_currentMillis(self):
        millis = currentMillis()
        self.assertTrue(type(millis) is int)

    def test_isCallable(self):
        self.assertFalse(isCallable(10))
        self.assertFalse(isCallable('str'))
        self.assertFalse(isCallable({}))
        self.assertFalse(isCallable(None))
        self.assertTrue(isCallable(clearEnv))

    def test_validateConfig(self):
        clearEnv()
        self.assertFalse(validateConfig())
        os.environ[NEXTAPM_LICENSE_KEY] = 'abc'
        self.assertFalse(validateConfig())
        os.environ[NEXTAPM_PROJECT_ID] = '1234'
        self.assertTrue(validateConfig())
        os.environ[NEXTAPM_LICENSE_KEY] = ''
        self.assertFalse(validateConfig())
        clearEnv()
        


