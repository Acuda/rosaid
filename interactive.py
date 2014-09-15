from core.CommandDispatcher import CommandDispatcher
from roshelper.Catkin import Catkin
from roshelper.Ros import Ros
import cmd

class HelpFormatter(object):

    def printHelp(self, lineList, firstAsCaption=True):
        assert isinstance(lineList, list)
        assert len(lineList) > 0

        print
        print 'Command:', lineList[0]
        if firstAsCaption:
            print '-'*len(lineList[0])
        for pline in lineList[1:]:
            print pline
        print


class StdCommands(object):

    def do_quit(self, line):
        return True

    def do_q(self, line):
        return True

    def reciveData(self, command_dispatcher):
        data = command_dispatcher.getData()
        if data:
            print data
            return True
        else:
            return False

    def printStdoutCommandDispatcher(self, command_dispatcher):
        while self.reciveData(command_dispatcher): pass

    def do_command(self, cmd):
        self.command_dispatcher.sendCmd(cmd)
        self.printStdoutCommandDispatcher(self.command_dispatcher)


class InteractiveCommands(cmd.Cmd, HelpFormatter, StdCommands):
    intro = "Interactive commands for ROS-AID-Tools"

    PARAMETER_WORKSPACE = object

    def postcmd(self, stop, line):
        return cmd.Cmd.postcmd(self, stop, line)

    def __init__(self, command_dispatcher, completekey='tab', stdin=None, stdout=None):
        cmd.Cmd.__init__(self, completekey, stdin, stdout)
        assert isinstance(command_dispatcher, CommandDispatcher)
        self.command_dispatcher = command_dispatcher
        self.parameter = dict()

    def do_set(self, line):
        lineList = line.split(' ', 1)
        if len(lineList) < 2:
            print 'to few arguments'
            return
        self.parameter[lineList[0]] = lineList[1]

    def do_print(self, _):
        print self.parameter

    def checkWorkspaceParameter(self):
        if self.PARAMETER_WORKSPACE not in self.parameter:
            self.parameter[self.PARAMETER_WORKSPACE] = '/home/fmw-be/sandbox/metric_tester'
            print '# WARNING!'
            print '# No workspace given, using <%s>' % '/home/fmw-be/sandbox/metric_tester'
            print

    def do_catkin(self, _):
        self.checkWorkspaceParameter()

        catkin = Catkin(self.command_dispatcher, self.parameter[self.PARAMETER_WORKSPACE])
        cc = CatkinCommands(catkin)
        cc.cmdloop()

    def do_ros(self, _):
        self.checkWorkspaceParameter()
        ros = Ros(self.command_dispatcher, self.parameter[self.PARAMETER_WORKSPACE])
        rc = RosCommands(ros)
        rc.cmdloop()

    def help_catkin(self):
        self.printHelp(['catkin WORKSPACE_PATH', 'switch to catkin tools for given workspace'])


class CatkinCommands(cmd.Cmd, HelpFormatter, StdCommands):

    def __init__(self, catkin, completekey='tab', stdin=None, stdout=None):
        cmd.Cmd.__init__(self, completekey, stdin, stdout)
        assert isinstance(catkin, Catkin)
        self.catkin = catkin

    def do_make(self, _):
        self.catkin.makeWorkspace()
        self.printStdoutCommandDispatcher(self.catkin.command_dispatcher)

    def do_init(self, _):
        self.catkin.initWorkspace()
        self.printStdoutCommandDispatcher(self.catkin.command_dispatcher)

    def do_check(self, _):
        print 'workspace',
        print 'exist' if self.catkin.checkWorkspaceExist() else 'not available'

class RosCommands(cmd.Cmd, HelpFormatter, StdCommands):
    def __init__(self, ros, completekey='tab', stdin=None, stdout=None):
        cmd.Cmd.__init__(self, completekey, stdin, stdout)
        assert isinstance(ros, Ros)
        self.ros = ros

    def do_source(self, line):
        print 'LINE: <%s>' % line
        if line == 'global':
            print 'source global environment'
            self.ros.sourceGlobalSetup()
        if line in ['workspace', 'local']:
            print 'source workspace/local environment'
            self.ros.sourceWorkspaceSetup()

    def help_source(self):
        self.printHelp(['source LOCATION', 'source the <global> setup.sh or the <workspace/local> setup.sh',
                        'Location can be:', '  global', '  workspace, local'])


if __name__ == '__main__':
    command_dispatcher = CommandDispatcher(timeout=1)
    interactiveCommands = InteractiveCommands(command_dispatcher)
    interactiveCommands.cmdloop()