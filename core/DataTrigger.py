import re


class DataTrigger(object):

    def __init__(self):
        self.recomp = re.compile('Could not find a configuration file for package (.*)\\.')
        self.foundList = list()


    def checkData(self, data):
        res = self.recomp.findall(data)

        if len(res):
            self.foundList.extend(res)
            print self.foundList