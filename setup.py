import urllib2
import re
import tempfile
import os
import sys
from shutil import rmtree
from subprocess import check_call
from distutils.core import run_setup

ASSIMP_CMAKE_URL = 'http://raw.github.com/assimp/assimp/master/CMakeLists.txt'
ASSIMP_URL       = 'https://github.com/assimp/assimp.git'
ASSIMP_PYTHON    = 'port/PyAssimp'

def get_assimp_version():
    cmakelists = urllib2.urlopen(ASSIMP_CMAKE_URL).read()
    major = int(re.findall('(?<=ASSIMP_VERSION_MAJOR) \d', cmakelists)[0])
    minor = int(re.findall('(?<=ASSIMP_VERSION_MINOR) \d', cmakelists)[0])
    patch = int(re.findall('(?<=ASSIMP_VERSION_PATCH) \d', cmakelists)[0])
    return major, minor, patch
     
def install_assimp():
    temp_dir = tempfile.mkdtemp()
    cwd      = os.getcwd()
    try:
        check_call(['git', 'clone', ASSIMP_URL, temp_dir])
        os.chdir(temp_dir)
        check_call(['cmake', '.'])
        check_call(['make'])
        check_call(['make', 'install'])
        os.chdir(os.path.join(temp_dir, ASSIMP_PYTHON))
        check_call(['python', 'setup.py', 'install'])
    finally:
        os.chdir(cwd)
        rmtree(temp_dir)

if __name__ == '__main__':
    if 'install' in sys.argv: install_assimp()
