"""
cmdhandler module is where all of the logic goes for the basic operations that
you can do on the kvs store 
"""
import sys
import re
from twisted.internet import reactor

class CommandHandler(object):
    """
    base handler class that holds all of the possible operations that can be 
    done on the key/value store implemented.
    """

    def __init__(self):
        self.data = {}

    def SET(self, key, value):
        """
        set the key to the value specified
        """
        self.data[key] = value
        return '+OK'

    def GET(self, key):
        """
        retrieve the value of the key specified
        """
        if not key in self.data:
            raise Exception('invalid key %s' % key)

        return '+%s' % self.data[key]

    def DEL(self, key):
        """
        delete the key and associated value from the kvs store
        """
        if not key in self.data:
            raise Exception('invalid key %s' % key)
        
        del self.data[key]
        return '+OK'

    def SHUTDOWN(self):
        """
        shutsdown the kvs store
        """
        reactor.stop()

    def RESET(self):
        """
        reset the kvs store and remove all of the keys and values currently in 
        the store
        """
        self.data.clear()
        return '+OK'

    def KEYS(self, key_reg_ex):
        """
        returns all of the key names that match the regular expression passed
        as an argument
        """
        keys = []
        for key in self.data:
            if re.match(key_reg_ex, key):
                keys.append(key)

        return '*%d\r\n%s' % (len(keys), '\r\n'.join(keys))


