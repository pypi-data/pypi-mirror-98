import nextapm.lib.logger as logger
from nextapm.lib.util import validateConfig
from nextapm.lib.constants import *
import os
import json
import requests

def sendData(data):
    if not validateConfig():
        return
  
    if data is None or type(data) is not dict:
        logger.error('[sendData] empty data passed', data)
        return

    try:
        logger.debug('[sendData] Data', data)
        host = os.getenv(NEXTAPM_HOST, DEFAULT_COLLECTOR)
        licenseKey = os.getenv(NEXTAPM_LICENSE_KEY)
        projectId = os.getenv(NEXTAPM_PROJECT_ID)
        queryParams = 'licenseKey='+licenseKey+'&projectId='+projectId
        url = host+'/api/data?'+queryParams
        payload = json.dumps(data)
        headers = {'content-type': 'application/json'}
        response = requests.post(url, data=payload, headers=headers)
        logger.info('collector response '+ json.dumps(response.json()))
    except Exception as exc:
        logger.error('req error ', exc)

    

def sendMetrics(txn):
    try:
        logger.debug('[sendMetric]')
        if not validateConfig():
            return False

        if txn is None:
            logger.error('[sendMetric] invalid txn')
            return False

        if not txn.isCompleted():
            logger.warn('[sendMetric] txn not completed')
            return False

        sendData({
            'info': {
              'agent_version': AGENT_VERSION
            },
            'txn': txn.getAsJson()
        })
    except Exception as e:
        logger.error('[sendMetric]', e)

    return False
