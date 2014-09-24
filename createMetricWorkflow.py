from core.CommandDispatcher import CommandDispatcher
from roshelper.Catkin import Catkin
from roshelper.Ros import Ros
from roshelper.RosTest import RosTest
from core.StdIOHandler import StdIOHandler
from core.DataTrigger import DataTrigger
from core import OSHelper
from roshelper import DefaultPathsAndCommands as DPAC
import os


def reciveData(command_dispatcher):
    data = command_dispatcher.getData()
    if data:
        print data
        return True
    else:
        return False

def reciveAllData(command_dispatcher):
    while reciveData(command_dispatcher): pass

def doWorkflow():

    workspace = '/home/fmw-be/sandbox/metric_tester'
    pkg_name = 'metric_suite_startup'
    #pkg_name = 'jenkins_test_repro'
    pkg_dependencies = ['rostest', 'rospy']

    OSHelper.rm_rf(workspace)

    cd = CommandDispatcher(timeout=5)
    catkin = Catkin(cd, workspace)
    ros = Ros(cd, workspace)

    dataTrigger = DataTrigger()

    ioh = StdIOHandler(timeout=5)
    ioh.addCommandDispatcher(cd)
    ioh.registerDataClient(dataTrigger.checkData)
    ioh.enableWatch()

    # create catkin workspace

    if not catkin.checkWorkspaceExist():
        catkin.initWorkspace()

    catkin.makeWorkspace()
    ros.sourceWorkspaceSetup()

    catkin.switchToSourceDirectory()

    # create catkin sub-pkg

    catkin.createPackage(pkg_name, pkg_dependencies)

    #cd.sendCmd('git clone https://github.com/ipa320/cob_object_perception.git')

    package_path = os.path.join(workspace, DPAC.PATH.CATKIN_SOURCE_DIRECTORY, pkg_name)
    rostest = RosTest(cd, package_path)
    rostest.createDirectorys()

    catkin.makeWorkspace()

    print package_path
    cd.sendCmd('ls %s' % package_path)


if __name__ == '__main__':
    doWorkflow()