"""
   Slack related helper methods and objects
"""
import logging
import os
import re
import shutil

from videotools import COMMANDS

logger = logging.getLogger('git')

PDIHUB = 'pdihub.hi.inet'
GITHUB = 'github.com'

GITHUB_URL = 'https://github.com'
GITHUB_URL_API = '%s/api/v3' % GITHUB_URL
GIT_SERVER_SSH = f'git@{GITHUB}'
GIT_DEVELOPMENT_BRANCH = 'develop'
GIT_RELEASE_BRANCH = 'master'

# context inside API URL for organizations
GIT_API_CONTEXT_ORGS = 'orgs'

# context inside API URL for users
GIT_API_CONTEXT_USERS = 'users'

# contexts inside and organization
GIT_API_CONTEXT_REPOS = 'repos'

# context pull requests
GIT_API_CONTEXT_PULLREQUESTS = 'pulls'

GIT_REPOS_JSON_KEY_NAME = 'name'
GIT_REPOS_JSON_KEY_SSH_URL = 'ssh_url'
GIT_REPOS_JSON_KEY_CLONE_URL = 'clone_url'

DEFAULT_ORIGIN_ORGANIZATIONS = ['videotools', 'st2v']
TELEFONICA_ORGANIZATION = 'Telefonica'


# -- regex to match url in .git/config files
RGX_GITURL = r'(?P<init>\s*url\s*=\s*)(?P<protocol>http:\/\/|https:\/\/|git@)(?P<server>(\w+\.)+\w+)' \
             r'(?P<separator>\/|:)(?P<organization>\w+)\/(?P<repository>.*)(\.git)'
PATTERN_GITURL = re.compile(RGX_GITURL)


DEFAULT_RENAME = 'REPOSITORY'


def match_url_regex(line):
    """
    Tries to match supplied line with some form of git config url, that is ssh or https, and provides a tuple
    with server name, organization and repository name
    :param line: line to match regex against with
    :return: If matches, a tuple as init, servername, organization and repository, or None if no match
    """
    logger.debug('matching [%s] with git url regex...', line)
    _match = PATTERN_GITURL.match(line)
    if _match:
        init = _match.group('init')
        protocol = _match.group('protocol')
        server = _match.group('server')
        separator = _match.group('separator')
        organization = _match.group('organization')
        repository = _match.group('repository')

        logger.debug(f'\t git url found')
        logger.debug(f'\t\t init -> %s', init)
        logger.debug(f'\t\t protocol -> %s', protocol)
        logger.debug(f'\t\t server -> %s', server)
        logger.debug(f'\t\t separator -> %s', separator)
        logger.debug(f'\t\t organization -> %s', organization)
        logger.debug(f'\t\t repository -> %s', repository)

        return init, protocol, server, separator, organization, repository
    else:
        return None


def migrate_from_pdihub(**kwargs):
    """
    Searches for git repositories and changes git/config address from old pdihub uris to github
    :param kwargs: optional arguments
                   localpath: Initial path to search for repositories to migrate
                      dryrun: Common option to all scripts
                      origin: pdihub organizations to match in original git config
                      target: final github organization to migrate the repositories into
                      rename: Rename directory to match repository name
    """
    localpath = os.path.expanduser(kwargs.get('localpath', os.path.curdir))
    dryrun = kwargs.get('dryrun')
    origin = kwargs.get('origin')
    target = kwargs.get('target')
    rename = kwargs.get('rename')

    if not origin:
        origin = DEFAULT_ORIGIN_ORGANIZATIONS

    logger.info('looking for repositories to migrate to github in [%s]...', localpath)
    logger.debug('\t original organizations --> %s', origin)
    logger.debug('\t   target  organization --> %s', target)

    for _item in [os.path.join(localpath, _it) for _it in os.listdir(localpath) if
                  os.path.isdir(os.path.join(localpath, _it)) and
                  os.path.exists(f'{os.path.join(localpath, _it)}/.git/config')]:

        _gitconfig_file = f'{_item}/.git/config'
        logger.debug('\t reading [%s]...', _gitconfig_file)
        with open(_gitconfig_file, 'r') as _file:
            _gitconfig_content = [line.strip('\n') for line in _file.readlines() if line]

        changes = False
        for _line in _gitconfig_content:
            _groups = match_url_regex(_line)
            if not _groups:
                continue

            _init = _groups[0]
            _protocol = _groups[1]
            _server = _groups[2]
            _separator = _groups[3]
            _organization = _groups[4]
            _repository = _groups[5]

            # check if server is pdihub
            if _server != PDIHUB:
                logger.debug('\t server does not match pdihub [%s]', _server)
                continue

            logger.info('\t checking urls in repository [%s]....', _item)
            # replace org and process next _item
            logger.debug('origin %s', origin)
            for _org in origin:
                if _organization == _org:
                    logger.debug('\t\t replacing [%s] in [%s] for [%s] ...', _org, _item, target)
                    new_url = f'{_init}{_protocol}{GITHUB}{_separator}{target}/{_organization}-{_repository}.git'
                    logger.info('\t\t from --> [%s]....', _line.strip())
                    logger.info('\t\t to --> [%s]....', new_url.strip())
                    _gitconfig_content[_gitconfig_content.index(_line)] = new_url
                    changes = True
                    break

        # if changes exists, save file
        if changes:
            logger.info('\t saving changes into [%s] ...', _gitconfig_file)
            if not dryrun:
                with open(_gitconfig_file, 'w') as _file:
                    for _line in _gitconfig_content:
                        _file.write(f'{_line}\n')
                    _file.flush()
                logger.info('\t\t %s SAVED', _gitconfig_file)

            if rename:
                base_name = os.path.basename(_item)
                dir_name = os.path.dirname(_item)
                new_dir_name = f'{_organization}-{_repository}'
                logger.info('\t renaming directory to match repository name...')
                logger.info('\t\t from --> %s', base_name)
                logger.info('\t\t  to  --> %s', new_dir_name)
                if not dryrun:
                    os.rename(_item, os.path.join(dir_name, new_dir_name))
                    logger.info('\t\t %s RENAMED', base_name)
    return ''


def init_parser(parent_parser):
    git_parser = parent_parser.add_parser(COMMANDS.GIT, help='Actions to manage team repositories')
    git_subparser = git_parser.add_subparsers()
    git_subparser.required = True

    # -- new key
    cmd_migrate = git_subparser.add_parser('migrate', help='Migrate config of local repositories to new organization')
    cmd_migrate.set_defaults(func=migrate_from_pdihub)
    cmd_migrate.add_argument('--localpath', dest='localpath', required=False, default=os.path.curdir)
    cmd_migrate.add_argument('--target', default='Telefonica', required=False)
    cmd_migrate.add_argument('--rename', action='store_true', default=False, required=False)
    cmd_migrate.add_argument('origin', nargs='*')

    return git_parser


def command(args):
    """
    Process the call in a script with supplied args
    """
    # copy of arguments for function
    cmd_args = vars(args).copy()

    # remove function from copied args
    del cmd_args['func']

    # execute func and print output
    print(args.func(**cmd_args))
