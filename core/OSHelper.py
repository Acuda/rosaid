import os
import errno

def mkdirs(path):
    try:
        print 'creating path', path
        os.makedirs(path)
    except OSError as ex:  # skip error if directory already exists
        if ex.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise ex
