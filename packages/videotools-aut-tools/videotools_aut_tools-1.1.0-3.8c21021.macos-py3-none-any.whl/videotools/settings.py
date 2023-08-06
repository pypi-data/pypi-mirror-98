"""
This module is the canonical way to share global information across modules
"""
import json
import logging.config
import os
from argparse import ArgumentParser
from collections import namedtuple

import coloredlogs
import urllib3

from videotools import APP_KEY_FILE, APP_CONFIG_FILENAME, get_resource_path, \
    APP_LOGGING_FILENAME, APP_LOGLEVEL, ResourceNotFoundException
from videotools.commands.cipher import decrypt

# -- disable verify=False warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# -- github token
GITHUB_TOKEN = None
DECRYPTED_GITHUB_TOKEN = None

# -- appconfig

_CONFIG_NAMES = {'GITHUB_TOKEN': 'github_token', "ADMIN_ROLE": "admin_role"}
CONFIG_FIELDS = namedtuple('ConfigFields', _CONFIG_NAMES.keys())(**_CONFIG_NAMES)

# -- ROLE
# - this role is used to check what actions a user can perform with the tools
ADMIN_ROLE = None

def get_common_parser():
    """
    Provides the common argument parser to be used in any args parser for our scripts
    :return: An instance of Argument parser with common args to any script
    """
    parser = ArgumentParser()
    parser.add_argument('--keyfile', '-KF',
                        help='Optional key file for cypher',
                        dest='keyfile',
                        action='store',
                        required=False)
    parser.add_argument('--dry-run', '-DR',
                        help='Do not perform any final action, just inform',
                        dest='dryrun',
                        action='store_true',
                        default=False,
                        required=False)
    return parser


# -- load config
class AppConfigNotFoundException(Exception):
    """
    Exception launched when application config is not found
    """


class NotGithubTokenException(Exception):
    """
    Exception launched when github token is missing from configuration
    """


# -- init logging
_log_config_file = get_resource_path(APP_LOGGING_FILENAME)
with open(_log_config_file, 'r') as file_:
    logging.config.dictConfig(json.loads(file_.read()))
    logging.root.setLevel(APP_LOGLEVEL)
coloredlogs.install(level=APP_LOGLEVEL)


# -- conf methods

def load_config():
    """
    Loads the content of application appconfig.json file as a dictionary
    """
    global GITHUB_TOKEN, DECRYPTED_GITHUB_TOKEN, ADMIN_ROLE

    _logger = logging.getLogger('settings')

    # -- create paths and save config files if not exists

    _logger.debug('checking if supplied file [%s] exists...', APP_CONFIG_FILENAME)
    _cfg_file = get_resource_path(APP_CONFIG_FILENAME)
    if not os.path.exists(_cfg_file):
        raise AppConfigNotFoundException(f'Configuration file not found: __{_cfg_file}__')

    # load de file
    _logger.debug('loading config...')
    with open(_cfg_file, 'r') as f:
        data = json.loads(f.read())
        _logger.debug('\t json config [%s]', data)

    _logger.debug('\t checking if token exists in config...')
    GITHUB_TOKEN = data.get(CONFIG_FIELDS.GITHUB_TOKEN)

    # check that aura token exists
    if not GITHUB_TOKEN:
        raise NotGithubTokenException('Missing github token in configuration')
    _logger.debug('\t\t OK')

    ADMIN_ROLE = data.get(CONFIG_FIELDS.ADMIN_ROLE) or None

    # in case pass file exists, decode the token
    try:
        if get_resource_path(APP_KEY_FILE):
            _logger.debug('decrypting github token with pass from __%s__', APP_KEY_FILE)
            DECRYPTED_GITHUB_TOKEN = decrypt(text_to_decrypt=GITHUB_TOKEN)
            _logger.debug('\t OK')
            if ADMIN_ROLE:
                _logger.debug('setting admin role....')
                ADMIN_ROLE = decrypt(text_to_decrypt=ADMIN_ROLE)
                _logger.debug('\t OK')
    except ResourceNotFoundException:
        _logger.debug('\t pass file not found, not decrypting github token')


load_config()
