"""
kvs server entry point
"""

from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor

from kvs.cmdhandler import CommandHandler

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

        self.lineReceived = self._start_command

    def _start_command(self, line):
        """
        parse the first line of the command which is the asterisk followed by 
        the number of lines that compose this operation
        """
        assert line.startswith('*'), 'got %s' % line

        # new command starting
        if self.start_command:
            self.sendLine('-unexpected start of new command\r')

        self.expected_arguments = int(line[1:])
        self.args = []

        self.lineReceived = self._read_command
        self.start_command = True

    def _read_command(self, line):
        """
        reads the command name and then sets up the method to parse the 
        remaining arguments
        """
        line = line.strip()
        self.command = line
        self.expected_arguments -= 1
        self.lineReceived = self._read_arguments

        if self.expected_arguments == 0:
            self._execute_command()

    def _read_arguments(self, line):
        """
        reads all of the arguments and then proceeds to execute it and return
        the state machine back to the start
        """
        # remove the command name from the arguments
        line = line.strip()
        self.args.append(line)
        self.expected_arguments -= 1

        if self.expected_arguments == 0:
            self._execute_command()

    def _execute_command(self):
        """
        executes the command and resets the state machine
        """
        # lookup the method handler
        if self.command in self._cmd_names:
            func = getattr(self._cmdhandler, self.command)
            try :
                result = func(*self.args)
                self.sendLine('%s' % result)
            except Exception as e:
                self.sendLine('-%s' % e)
        else:
            self.sendLine('-unknown command %s' % self.command)

        self.start_command = False
        self.lineReceived = self._start_command

           
class CommandReaderFactory(Factory):
    """
    factory class required by reactor
    """

    def __init__(self, cmdhandler):
        self._cmdhandler = cmdhandler

    def buildProtocol(self, addr):
        return CommandReader(self._cmdhandler)

_PORT = 9999

def main():
    """
    main entry function
    """
    print('kvs listening at localhost:%d' % _PORT)
    reactor.listenTCP(_PORT, CommandReaderFactory(CommandHandler()))
    reactor.run()

if __name__ == '__main__':
    main()

