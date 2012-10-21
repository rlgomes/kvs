
import unittest

from base import BaseTest

class ProtocolTest(BaseTest):

    def test_basic_set_and_get(self):
        """
        simple set and get test
        """
        self.SET('A', 100)
        resp = self.GET('A')
        assert resp == '100', 'expected 100 got %s' % resp

    def test_get_inexistent(self):
        """
        verify that inexistent key comes back as such
        """
        resp = self.GET('X')
        assert resp == 'invalid key X', 'got %s' % resp

    def test_del_inexistent(self):
        """
        verify that deleting an inexistent key comes back as such
        """
        resp = self.DEL('X')
        assert resp == 'invalid key X', 'got %s' % resp

    def test_set_get_and_del(self):
        """
        verify that you can set a key retrieve followed by deleting it and 
        not being able to retrieve it any longer
        """
        self.SET('B', 100)
        resp = self.GET('B')
        assert resp == '100', 'expected 100 got %s' % resp

        self.DEL( 'B')
        resp = self.GET('B')
        assert resp == 'invalid key B', 'got %s' % resp

    def test_basic_multiple_key_set_and_get(self):
        """
        multiple set and get test
        """
        self.SET('key1', 'value1')
        self.SET('key2', 'value2')
        value1 = self.GET('key1')
        value2 = self.GET('key2')
        assert value1 == 'value1', 'expected value1 got %s' % value1
        assert value2 == 'value2', 'expected value2 got %s' % value2

    def test_verify_reset(self):
        """
        verify that reset in fact removes all existing keys
        """
        keys = self.KEYS('.*')
        assert len(keys) != 0, 'expected some keys in the store, but got none'

        self.RESET()
        keys = self.KEYS('.*')
        assert len(keys) == 0, 'expected no keys in the store, but foudn %s' % keys

if __name__ == '__main__':
    unittest.main()

