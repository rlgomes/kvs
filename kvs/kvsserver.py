
from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor


class CommandReader(LineReceiver):
    """
    state machine comand reader 
    """

    def __init__(self, cmdhandler):
        self._cmdhandler = cmdhandler
        self._cmd_names = dir(cmdhandler)

        self.start_command = False
        self.reading_argument_size = False
        self.expected_arguments = -1
        self.args = []
       
    def lineReceived(self, line):
        if line.startswith('*'):
            # new command starting
            if self.start_command:
                self.sendLine('-unexpected start of new command\r')

            self.start_command = True
            self.expected_arguments = int(line[1:])
            self.args = []
            return 
        
        if self.start_command:
            # we're still reading the arguments
            line = line.strip()
            self.args.append(line)
            self.expected_arguments -= 1

        if self.expected_arguments == 0:
            # lookup the method handler
            command = self.args[0]

            # remove the command name from the arguments
            self.args = self.args[1:]

            if command in self._cmd_names:
                func = getattr(self._cmdhandler, command)
                result = func(*self.args)
                self.sendLine('+%s' % result)
            else:
                self.sendLine('-unknown command %s' % command)

            self.start_command = False

class CommandReaderFactory(Factory):

    def __init__(self, cmdhandler):
        self._cmdhandler = cmdhandler

    def buildProtocol(self, addr):
        return CommandReader(self._cmdhandler)

class CommandHandler(object):
    
    def __init__(self):
        self.data = {}

    def set(self, key, value):
        self.data[key] = value
        return 'OK'

    def get(self, key):
        return self.data[key]

_PORT = 9999

def main():
    print('kvs listening at localhost:%d' % _PORT)
    reactor.listenTCP(_PORT, CommandReaderFactory(CommandHandler()))
    reactor.run()

