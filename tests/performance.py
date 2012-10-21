"""
"""
import time
import unittest

from base import BaseTest

class PerformanceTest(BaseTest):

    def test_1st_set_small_key_performance(self):
        """
        """
        start = time.time()
        for index in range(0,20000):
            self.send('SET', 'key-%d' % index, 'tiny little value')
        elapsed = time.time() - start
        print('\nSET %f ops/sec' % (1000/elapsed))

    def test_2nd_get_small_key_performance(self):
        """
        """
        start = time.time()
        for index in range(0,20000):
            self.send('GET', 'key-%d' % index)
        elapsed = time.time() - start
        print('\nGET %f ops/sec' % (1000/elapsed))

    def test_3rd_del_small_key_performance(self):
        """
        """
        start = time.time()
        for index in range(0,20000):
            self.send('DEl', 'key-%d' % index)
        elapsed = time.time() - start
        print('\nDEL %f ops/sec' % (1000/elapsed))

if __name__ == '__main__':
    unittest.main()

