import os
from core import OSHelper
from core.CommandDispatcher import CommandDispatcher
from roshelper import DefaultPathsAndCommands as DPAC


class Catkin(object):

    def __init__(self, command_dispatcher, workspace_path):
        assert isinstance(command_dispatcher, CommandDispatcher)
        self.command_dispatcher = command_dispatcher
        self.workspace_path = workspace_path
        self.workspace_src_path = os.path.join(self.workspace_path, DPAC.PATH.CATKIN_SOURCE_DIRECTORY)

    def initWorkspace(self):
        OSHelper.mkdirs(self.workspace_src_path)

        self.command_dispatcher.sendCmd(DPAC.CMD.CD % self.workspace_src_path)
        self.command_dispatcher.sendCmd(DPAC.CMD.SOURCE % DPAC.PATH.GLOBAL_SOURCE_SETUP_FILE)
        self.command_dispatcher.sendCmd(DPAC.CMD.CATKIN_INIT_WORKSPACE)

    def checkWorkspaceExist(self):
        return os.path.exists(self.workspace_path) and os.path.exists(self.workspace_src_path)

    def makeWorkspace(self):
        self.command_dispatcher.sendCmd(DPAC.CMD.CD % self.workspace_path)
        self.command_dispatcher.sendCmd(DPAC.CMD.CATKIN_MAKE)


