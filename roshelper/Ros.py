from core.CommandDispatcher import CommandDispatcher
from roshelper import DefaultPathsAndCommands as DPAC


class Ros(object):

    def __init__(self, command_dispatcher, workspace_path):
        assert isinstance(command_dispatcher, CommandDispatcher)
        self.command_dispatcher = command_dispatcher
        self.workspace_path = workspace_path

    def sourceWorkspaceSetup(self):
        self.command_dispatcher.sendCmd(DPAC.CMD.CD % self.workspace_path)
        self.command_dispatcher.sendCmd(DPAC.CMD.SOURCE % DPAC.PATH.WORKSPACE_SOURCE_SETUP_FILE)

    def sourceGlobalSetup(self):
        self.command_dispatcher.sendCmd(DPAC.CMD.SOURCE % DPAC.PATH.GLOBAL_SOURCE_SETUP_FILE)

