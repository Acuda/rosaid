from core.CommandDispatcher import CommandDispatcher
from roshelper import DefaultPathsAndCommands as DPAC
from core import OSHelper
import os

class RosTest(object):

    def __init__(self, command_dispatcher, package_path):
        assert isinstance(command_dispatcher, CommandDispatcher)
        self.command_dispatcher = command_dispatcher
        self.package_path = package_path

    def createDirectorys(self):
        absPath = [os.path.join(self.package_path, dir) for dir in DPAC.PATH.DEFAULT_PACKAGE_FOLDER]
        map(OSHelper.mkdirs, absPath)
