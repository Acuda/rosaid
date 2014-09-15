import threading
import re
import os
import time
from core.CommandDispatcher import CommandDispatcher


class StdIOHandler(threading.Thread):

    def __init__(self, timeout=5):
        threading.Thread.__init__(self)
        self.registredDataClients = list()
        self.dispatcherList = list()
        self.msgData = list()
        self.doRun = False
        self.timeout = timeout
        self.printData = True

    def run(self):
        while self.doRun:
            for dispatcher in self.dispatcherList:
                data = self.reciveData(dispatcher)

                if not len(data):
                    continue

                self.lastData = time.time()
                self.handleData(data)

            if time.time() - self.lastData > self.timeout:
                self.doRun = False
            else:
                time.sleep(self.sleepTime)

    def handleData(self, dataList):
        self.msgData.extend(dataList)
        if self.printData:
            print os.linesep.join(dataList)
        self.notifyDataClients(dataList)

    def registerDataClient(self, client_fnc):
        self.registredDataClients.append(client_fnc)

    def notifyDataClients(self, dataList):
        for client in self.registredDataClients:
            for data in dataList:
                client(data)


    def addCommandDispatcher(self, command_dispatcher):
        self.dispatcherList.append(command_dispatcher)

    def reciveData(self, command_dispatcher):
        assert isinstance(command_dispatcher, CommandDispatcher)
        command_dispatcher.dataAvailable()
        data = command_dispatcher.getData(getAsList=True, skipWait=True)
        return data

    def enableWatch(self, seconds=0.2):
        self.sleepTime = seconds
        self.doRun = True
        self.lastData = time.time()
        self.start()


if __name__ == '__main__':

    stdio = StdIOHandler()
    stdio.enableWatch()

