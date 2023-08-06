from ..data.context import setCurTxn, getCurTxn
from ..data.txn import Transaction
from ..constants import classNameKey, methodNameKey, preHookKey, postHookKey

def captureTxn(args, kwargs):
    txn = Transaction()
    setCurTxn(txn)

def endTxn(args, kwargs):
    txn = getCurTxn()
    if txn is None or args is None:
        return

    if len(args) <= 0:
        return

    obj = args[0]
    if obj is None:
        return
    
    if hasattr(obj,'path'):
        txn.setUrl(getattr(obj,'path'))
    
    if hasattr(obj,'command'):
        txn.setMethod(getattr(obj, 'command'))

    txn.end()


def extractStatusCode(args, kwargs):
    txn = getCurTxn()
    if txn is None or args is None:
        return

    if len(args) <= 1:
        return
    
    txn.setStatus(args[1])


modulesInfo = {
  'http.server': [
      {
          classNameKey: 'BaseHTTPRequestHandler',
          methodNameKey: 'handle_one_request',
          preHookKey: captureTxn,
          postHookKey: endTxn
      },
      {
          classNameKey: 'BaseHTTPRequestHandler',
          methodNameKey: 'send_response',
          postHookKey: extractStatusCode
      }
  ]
}

