import urllib2
import re
import tempfile
import os
import sys
import time
from shutil import rmtree
from subprocess import check_call

from distutils.core import setup
from distutils.command.build import build

ASSIMP_CMAKE_URL = 'http://raw.github.com/assimp/assimp/master/CMakeLists.txt'
ASSIMP_URL       = 'https://github.com/assimp/assimp.git'
ASSIMP_PYTHON    = 'port/PyAssimp'

def get_assimp_version():
    cmakelists = urllib2.urlopen(ASSIMP_CMAKE_URL).read()
    major = re.findall('(?<=ASSIMP_VERSION_MAJOR) \d', cmakelists)[0].strip()
    minor = re.findall('(?<=ASSIMP_VERSION_MINOR) \d', cmakelists)[0].strip()
    patch = re.findall('(?<=ASSIMP_VERSION_PATCH) \d', cmakelists)[0].strip()
    version_string = '.'.join([major, minor, patch])
    return version_string

def install_assimp():
    temp_dir = os.path.join(tempfile.gettempdir(), 'assimp_' + str(int(time.time())))
    os.makedirs(temp_dir)
    cwd      = os.getcwd()

    #try:
    check_call(['git', 'clone', ASSIMP_URL, temp_dir])
    os.chdir(temp_dir)
    check_call(['cmake', '.'])
    check_call(['make'])
    check_call(['make', 'install'])
    os.chdir(os.path.join(temp_dir, ASSIMP_PYTHON))
    check_call(['python', 'setup.py', 'install'])
    #finally:
    os.chdir(cwd)
    rmtree(temp_dir)
        
class _build(build):
    def run(self):
        install_assimp()

setup(
    name    = 'assimp_latest',
    description = 'assimp/pyassimp fresh off github',
    version = get_assimp_version(),
    cmdclass={'build': _build}
)
