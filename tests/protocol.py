
import socket
import unittest

class ProtocolTest(unittest.TestCase):

    def setUp(self):
        self._connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._connection.connect(('localhost', 9999))

    def tearDown(self):
        self._connection.close()

    def _send_cmd(self, cmd, *args):
        cmd_string = '*%d\r\n' % (len(args) + 1)
        cmd_string += '%s\r\n' % cmd

        for arg in args:
            arg = str(arg)
            cmd_string += '%s\r\n' % arg

        self._connection.sendall(cmd_string)
        return self._read_response().strip()

    def _read_response(self):
        status = self._connection.recv(1)

        response = ''
        read = self._connection.recv(1)
        while read != '\n':
            response += read
            read = self._connection.recv(1)

        if status == '+':
            # successful response with a single line response
           return response
        else:
            # unsucceful response with error message
            raise Exception(response)

    def test_basic_set_and_get(self):
        self._send_cmd('set', 'A', 100)
        resp = self._send_cmd('get', 'A')
        assert resp == '100', 'expected 100 got %s' % resp
        
if __name__ == '__main__':
    unittest.main()

