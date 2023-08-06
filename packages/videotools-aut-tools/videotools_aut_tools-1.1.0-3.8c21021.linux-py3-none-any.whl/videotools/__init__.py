"""
 Python __init__ file for package config
"""
import logging.config
import os
from collections import namedtuple
from logging.handlers import TimedRotatingFileHandler
from distutils.util import strtobool

import requests
from dotenv import load_dotenv

# -- general props
DEFAULT_ENCODING = 'utf-8'
DEFAULT_TIMEZONE = 'Europe/Madrid'

VALID_LOG_LEVELS = {'DEBUG': logging.DEBUG, 'INFO': logging.INFO, 'WARNING': logging.WARNING, 'ERROR': logging.ERROR,
                    'CRITICAL': logging.CRITICAL}

# -- list of commands
_COMMAND_NAMES = {'CIPHER': 'cipher', 'GIT': 'git'}
COMMANDS = namedtuple('ConfigFields', _COMMAND_NAMES.keys())(**_COMMAND_NAMES)

# -- default values
# default dir with configuration files
APP_RESOURCES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources')

APP_LOGLEVEL_KEYNAME = 'VITOOLS_LOGLEVEL'

APP_HOME_DIR = os.path.expanduser('~/.vitools')
APP_LOG_DIR = os.path.join(APP_HOME_DIR, 'log')
APP_ENV_FILE = os.path.join(APP_HOME_DIR, '.env')
APP_KEY_FILE = os.path.join(APP_HOME_DIR, '.key')
APP_CONFIG_FILENAME = 'appconfig.json'
APP_LOGGING_FILENAME = 'applogging.json'


# -- helper methods

def get_envar(key, default=None):
    return os.environ.get(key, default)


def is_url_available(url, verify=True, timeout=10):
    """
    Check if url can be reached
    :param url: URL address
    :param verify: Don't perform verification of remote certificate
    :param timeout: Time to wait for response before quitting
    :return: True if can be reached, False otherwise
    """
    response = requests.get(url, verify=verify, timeout=timeout)
    return response.ok


class ResourceNotFoundException(Exception):
    """
    Exception launched when local resource name is not found under resources's look path
    """


def get_resource_path(resource_name):
    """
    Searches for resources in home app path or  default resources dir
    :param resource_name:  Name of the resource to look for
    :return: The founded resource path. A ResourceNotFoundException is thrown otherwise
    """
    try:
        if not resource_name:
            raise ResourceNotFoundException('resource_name can not be empty')

        # check home dir and finally library resources
        for _path in [resource_name, os.path.join(APP_HOME_DIR, resource_name),
                      os.path.join(APP_RESOURCES_DIR, resource_name)]:
            if os.path.isabs(_path) and os.path.exists(_path):
                return _path
        raise ResourceNotFoundException(f'could not find __{resource_name}__ resource')
    except Exception as ex:
        raise ResourceNotFoundException(f'resource name: [{resource_name}] not found', ex)


# -- custom logging class
class AppFileHandler(TimedRotatingFileHandler):
    def __init__(self, filename, **kwargs):
        super().__init__(os.path.join(APP_LOG_DIR, filename), **kwargs)


# =======================
#        INIT
# =======================


# -- init .env vars
if os.path.exists(APP_ENV_FILE):
    load_dotenv(APP_ENV_FILE)

DEBUG = strtobool(get_envar('VITOOLS_DEBUG', 'False'))
if DEBUG:
    APP_LOGLEVEL = logging.DEBUG
else:
    APP_LOGLEVEL = VALID_LOG_LEVELS.get(get_envar(APP_LOGLEVEL_KEYNAME, 'INFO'))

# -- create dirs if needed
for _path in (APP_HOME_DIR, APP_LOG_DIR):
    if not os.path.exists(_path):
        os.makedirs(_path)

# -- copy config files if needed
for _name in (APP_CONFIG_FILENAME, APP_LOGGING_FILENAME):
    _file = os.path.join(APP_HOME_DIR, _name)
    if not os.path.exists(_file):
        with open(get_resource_path(_name), 'r') as _fread:
            content = _fread.read()
            with open(_file, 'w') as _fwrite:
                _fwrite.write(content)
                _fwrite.flush()

# -- save env file if needed
if not os.path.exists(APP_ENV_FILE):
    with open(APP_ENV_FILE, 'w') as _file:
        _file.write('VITOOLS_DEBUG=False\n')
        _file.write('VITOOLS_LOGLEVEL=INFO\n')
        _file.flush()
