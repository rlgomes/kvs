"""
"""
import time
import unittest

from base import BaseTest

ITERATIONS=20000

class PerformanceTest(BaseTest):

    def test_1st_set_small_key_performance(self):
        """
        """
        start = time.time()
        for index in range(0, ITERATIONS):
            self.SET('key-%d' % index, 'tiny little value')
        elapsed = time.time() - start
        print('\nSET %f ops/sec' % (ITERATIONS/elapsed))

    def test_2nd_get_small_key_performance(self):
        """
        """
        start = time.time()
        for index in range(0, ITERATIONS):
            self.GET('key-%d' % index)
        elapsed = time.time() - start
        print('\nGET %f ops/sec' % (ITERATIONS/elapsed))

    def test_3rd_del_small_key_performance(self):
        """
        """
        start = time.time()
        for index in range(0, ITERATIONS):
            self.DEL('key-%d' % index)
        elapsed = time.time() - start
        print('\nDEL %f ops/sec' % (ITERATIONS/elapsed))

if __name__ == '__main__':
    unittest.main()

