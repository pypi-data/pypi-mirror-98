"""

"""
import platform
import os
import re
import sys
import errno
from shutil import copy2

# /users/me/Conductor/ciomaya
PKG_DIR = os.path.dirname(os.path.abspath(__file__))
MODULE_DIR = PKG_DIR
PKGNAME = os.path.basename(PKG_DIR)  # ciomaya
MODULE_FILENAME = "conductor.mod"
PLATFORM = sys.platform
with open(os.path.join(PKG_DIR, 'VERSION')) as version_file:
    VERSION = version_file.read().strip()


def main():
    if not PLATFORM in ["darwin", "win32", "linux"]:
        sys.stderr.write("Unsupported platform: {}".format(PLATFORM))
        sys.exit(1)

    module_dir = get_maya_module_dir()
    write_maya_mod_file(module_dir)
    sys.stdout.write("Completed Maya Module setup!\n")


def get_maya_module_dir():

    app_dir = os.environ.get( "MAYA_APP_DIR")
    if not app_dir:
        if PLATFORM == "darwin":
            app_dir = "~/Library/Preferences/Autodesk/maya"
        elif PLATFORM == "linux":
            app_dir = "~/maya"
        else:  # windows
            app_dir = "~\Documents\maya"
 
    return os.path.join(os.path.expanduser(app_dir), "modules")


def write_maya_mod_file(module_dir):
 
    ensure_directory(module_dir)
    fn = os.path.join(module_dir, MODULE_FILENAME)
    with open(fn, "w") as f:
        f.write("+ conductor {} {}\n".format(VERSION, MODULE_DIR))
        f.write("PYTHONPATH+:=../\n")

    sys.stdout.write("Wrote Maya module file: {}\n".format(fn))


def ensure_directory(directory):
    try:
        os.makedirs(directory)
    except OSError as ex:
        if ex.errno == errno.EEXIST and os.path.isdir(directory):
            pass
        else:
            raise


if __name__ == '__main__':
    main()
