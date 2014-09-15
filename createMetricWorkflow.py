from core.CommandDispatcher import CommandDispatcher
from roshelper.Catkin import Catkin
from roshelper.Ros import Ros
from core.StdIOHandler import StdIOHandler
from core.DataTrigger import DataTrigger
from core import OSHelper



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
    pkg_dependencies = ['rostest', 'rospy', 'cob_marker']

    OSHelper.rm_rf(workspace)



    cd = CommandDispatcher(timeout=5)
    catkin = Catkin(cd, workspace)
    ros = Ros(cd, workspace)

    dataTrigger = DataTrigger()

    ioh = StdIOHandler(timeout=30)
    ioh.addCommandDispatcher(cd)
    ioh.registerDataClient(dataTrigger.checkData)
    ioh.enableWatch()

    if not catkin.checkWorkspaceExist():
        catkin.initWorkspace()

    catkin.makeWorkspace()
    ros.sourceWorkspaceSetup()

    catkin.switchToSourceDirectory()

    catkin.createPackage(pkg_name, pkg_dependencies)

    cd.sendCmd('git clone https://github.com/ipa320/cob_object_perception.git')

    catkin.makeWorkspace()

    cd.sendCmd('pwd')

    print
    print
    print
    print


    print

if __name__ == '__main__':
    doWorkflow()