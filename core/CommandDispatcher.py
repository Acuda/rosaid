from subprocess import Popen, PIPE
import fcntl
import os
import time
from collections import deque

class CommandDispatcher(object):
    def __init__(self, command='/bin/bash', command_args=None, cwd=None, timeout=5, commandSleepTime=0.1):
        self.cmdSleepTime = commandSleepTime
        self.timeout = timeout

        args = list()
        args.append(command)
        if command_args:
            if isinstance(command_args, list):
                args.extend(command_args)
            else:
                args.append(command_args)

        self.proc = Popen(args, shell=False, stdin=PIPE, stdout=PIPE, cwd=cwd)
        fcntl.fcntl(self.proc.stdout.fileno(), fcntl.F_SETFL, os.O_NONBLOCK)  # switch to nonblocking mode
        self.outque = deque()


    def dataAvailable(self, ignore_stdin_que=False):
        try:
            data = self.proc.stdout.read().splitlines()
            self.outque.extend(data)
            time.sleep(self.cmdSleepTime)
            return True
        except IOError as ex:
            if ex.errno is 11:  # no data avail in non-blocking mode...
                return False if ignore_stdin_que else bool(len(self.outque))
            else:
                raise ex

    def getData(self, getAll=True):
        self.waitData()
        if getAll:
            data = os.linesep.join(self.outque)
            self.outque = deque()
            return data
        else:
            return self.outque.popleft()

    def waitData(self):
        waitStartTime  = time.time()
        while time.time() - waitStartTime < self.timeout and not self.dataAvailable(ignore_stdin_que=False):
            time.sleep(self.cmdSleepTime)

    def _sendCmdList(self, commandList):
        assert isinstance(commandList, list)
        for cmd in commandList:
            self.sendCmd(cmd)

    def sendCmd(self, command):
        if isinstance(command, list):
            self._sendCmdList(command)
            return
        cmd = ''.join([command, os.linesep])
        self.proc.stdin.write(cmd)
        time.sleep(self.cmdSleepTime)  # waiting for not breaking the pipe

