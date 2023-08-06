"""
List of contants for continuous integration operations
"""
import os

TOOLS_REPO = 'videotools-aut-tools'

SETUP_PY_FILENAME = 'setup.py'
DEFAULT_SETUP_PY_LOCATION = os.path.join(os.getcwd(), SETUP_PY_FILENAME)

SETUP_CFG_FILENAME = 'setup.cfg'
DEFAULT_SETUP_CFG_LOCATION = os.path.join(os.getcwd(), SETUP_CFG_FILENAME)

MANIFEST_IN_FILENAME = 'MANIFEST.in'
DEFAULT_MANIFEST_IN_LOCATION = os.path.join(os.getcwd(), MANIFEST_IN_FILENAME)

BUILD_DIRECTORY_NAME = 'build'
DEFAULT_BUILD_DIRECTORY_LOCATION = os.path.join(os.getcwd(), BUILD_DIRECTORY_NAME)

DIST_DIRECTORY_NAME = 'dist'
DEFAULT_DIST_DIRECTORY_LOCATION = os.path.join(os.getcwd(), DIST_DIRECTORY_NAME)

DEFAULT_COMMITTER_DICT = {'name': 'Agustin Escamez',
                          'email': 'agustin.escamezchimeno@telefonica.com'}

DEF_BRANCHES = ['master']

