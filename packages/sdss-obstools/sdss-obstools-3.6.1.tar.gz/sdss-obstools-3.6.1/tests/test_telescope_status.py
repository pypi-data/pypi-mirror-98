#!/usr/bin/env python3
import unittest
from pathlib import Path
from bin import telescope_status
import signal


class TestTelStatus(unittest.TestCase):
    def setUp(self):
        self.file = (Path(__file__).absolute().parent.parent
                     / 'bin/telescope_status.py')

    @staticmethod
    def handler(signum, frame):
        print('Exiting call')
        raise TimeoutError('The function reached timeout without other errors')

    def test_print(self):
        signal.signal(signal.SIGALRM, self.handler)
        signal.alarm(10)
        telescope_status.main()


if __name__ == '__main__':
    unittest.main()
