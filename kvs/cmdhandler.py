"""

"""

class CommandHandler(object):
    """
    base handler class that holds all of the possible operations that can be 
    done on the key/value store implemented.
    """
    def __init__(self):
        self.data = {}

    def set(self, key, value):
        """
        set the key to the value specified
        """
        self.data[key] = value
        return 'OK'

    def get(self, key):
        """
        retrieve the value of the key specified
        """
        if not key in self.data:
            raise Exception('invalid key %s' % key)

        return self.data[key]


