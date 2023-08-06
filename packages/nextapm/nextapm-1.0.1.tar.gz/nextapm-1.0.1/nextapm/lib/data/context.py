import threading

threadLocal = threading.local()

def setCurTxn(txn):
    setattr(threadLocal, 'NextApmCurTxn', txn)

def clearCurTxn():
    setCurTxn(None)

def getCurTxn():
    return getattr(threadLocal, 'NextApmCurTxn', None)

def isTxnActive():
    txn = getCurTxn()
    return txn is not None


