import os
import errno
import shutil

def mkdirs(path):
    try:
        print 'creating path', path
        os.makedirs(path)
    except OSError as ex:  # skip error if directory already exists
        if ex.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise ex

def rm_rf(path):

    try:
        shutil.rmtree(path)
    except OSError as ex:
        if ex.errno is not errno.ENOENT:
            raise ex