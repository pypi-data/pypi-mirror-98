import unittest
from .txn import Transaction

class TxnTest(unittest.TestCase):

    def test_end(self):
        txn = Transaction()
        txn.end()
        self.assertTrue(txn.isCompleted())
        self.assertTrue(txn.endTime > 0)
        self.assertTrue(txn.rt >= 0)

    def test_setUrl(self):
        txn = Transaction()
        url = txn.url
        txn.setUrl(10)
        self.assertEqual(txn.url, url)
        txn.setUrl(None)
        self.assertEqual(txn.url, url)
        txn.setUrl('/api')
        self.assertEqual(txn.url, '/api')

    def test_setMethod(self):
        txn = Transaction()
        method = txn.method
        txn.setMethod(10)
        self.assertEqual(txn.method, method)
        txn.setMethod(None)
        self.assertEqual(txn.method, method)
        txn.setMethod('POST')
        self.assertEqual(txn.method, 'POST')

    def test_setStatus(self):
        txn = Transaction()
        status = txn.status
        txn.setStatus('POST')
        self.assertEqual(txn.status, status)
        txn.setMethod(None)
        self.assertEqual(txn.status, status)
        txn.setMethod(200)
        self.assertEqual(txn.status, 200)

        
        
    