
import socket
import unittest

class BaseTest(unittest.TestCase):

    def setUp(self):
        self._connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._connection.connect(('localhost', 9999))

    def tearDown(self):
        self._connection.close()

    def SET(self, key, value):
        self._connection.sendall('*3\r\nSET\r\n%s\r\n%s\r\n' % (key, value))
        return self._read_response()

    def GET(self, key):
        self._connection.sendall('*2\r\nGET\r\n%s\r\n' %  key)
        return self._read_response()

    def DEL(self, key):
        self._connection.sendall('*2\r\nDEL\r\n%s\r\n' %  key)
        return self._read_response()

    def KEYS(self, regex):
        self._connection.sendall('*2\r\nKEYS\r\n%s\r\n' %  regex)
        return self._read_response()

    def RESET(self):
        self._connection.sendall('*1\r\nRESET\r\n')
        return self._read_response()

    def _read_line(self):
        response = ''
        read = self._connection.recv(1)
        while read != '\n':
            response += read
            read = self._connection.recv(1)

        return response

    def _read_response(self):
        status = self._connection.recv(1)

        if status == '+':
            # successful response with a single line response
            return self._read_line().strip()

        if status == '-':
            # unsucceful response with error message
            return self._read_line().strip()

        if status == '*':
            lines = int(self._read_line().strip())
            response = []
            for index in range(0, lines):
                line = self._read_line().strip()
                response.append(line)

            # successful multi-value response
            return response

if __name__ == '__main__':
    unittest.main()
