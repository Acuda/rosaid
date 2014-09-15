class PATH(object):
    GLOBAL_SOURCE_SETUP_FILE = '/opt/ros/hydro/setup.sh'
    WORKSPACE_SOURCE_SETUP_FILE = 'devel/setup.sh'
    CATKIN_SOURCE_DIRECTORY = 'src'

class CMD(object):
    # ROS
    SOURCE = 'source %s'  # source [sourced file]

    # CATKIN
    CATKIN_INIT_WORKSPACE = 'catkin_init_workspace'
    CATKIN_MAKE = 'catkin_make'
    CATKIN_CREATE_PACKAGE = 'catkin_create_pkg %s %s'  # catkin_create_pkg [PACKAGE_NAME] [DEP1 DEP2 ...]

    # LINUX
    CD = 'cd %s'  # cd <target dir>