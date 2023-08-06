#!python
"""
Script used as main cli executable to perform operations by Video Tools team
"""
import logging
import sys

__author__ = 'agustin.escamezchimeno@telefonica.com'

from videotools.commands import cipher, git
from videotools.settings import get_common_parser
from videotools.commands.cipher import COMMANDS


class VitoolsScript:

    def __init__(self, sys_args):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.script_args = self.__build_args(sys_args)

    def __build_args(self, sys_args):
        parser = None
        try:
            # build parser
            parser = VitoolsScript.init_parser()

            # let's check supplied params
            self.logger.debug('-----------------------------')
            self.logger.debug('\t Parsing sys arguments...  ')

            script_args = parser.parse_args(sys_args[1:])

            self.logger.debug('\t Argument PARSED [%s]', script_args)

            self.logger.debug('-----------------------------')
            return script_args
        except SystemExit:
            if '-h' not in sys_args:
                parser.print_help()
            sys.exit(0)
        except Exception:
            self.logger.exception('\t\t Error verifying arguments')
            sys.exit(-1)

    @staticmethod
    def init_parser():
        parser = get_common_parser()
        subparsers = parser.add_subparsers(dest='command')
        subparsers.required = True

        # add cipher command opts
        cipher.init_parser(subparsers)
        git.init_parser(subparsers)

        return parser

    def run(self):
        if self.script_args.command == COMMANDS.CIPHER:
            cipher.command(self.script_args)
        elif self.script_args.command == COMMANDS.GIT:
            git.command(self.script_args)


def init():
    """
    Initialization method added to be able to tests correct script invocation
    :return: Whatever exit from run method
    """
    if __name__ == "__main__":
        script = VitoolsScript(sys.argv)
        sys.exit(script.run())


init()
