import unittest
from .txn import Transaction
from .context import clearCurTxn, setCurTxn, getCurTxn, isTxnActive


class ContextTest(unittest.TestCase):

    def test_context(self):
        self.assertEqual(getCurTxn(), None)
        self.assertFalse(isTxnActive())
        txn = Transaction()
        setCurTxn(txn)
        self.assertEqual(getCurTxn(), txn)
        self.assertTrue(isTxnActive())
        clearCurTxn()
        self.assertEqual(getCurTxn(), None)
        self.assertFalse(isTxnActive())