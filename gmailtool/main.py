# -*- coding: utf-8 -*-
"""Main entry point for gmailtool"""

import argparse
import gmailtool.argument_parser
import gmailtool.auth
import logging
import os
import sys


logger = logging.getLogger('gmailtool')


def register_sub_commands(parsers, environ):
    """Register sub commands

    This function calls the register commands fucntion associated with
    each sub command.

    Args:
        parsers (Arguement Parsers Object): Object to use to add parsers for commands
        environ (dict): The environment dictionary
    """
    gmailtool.auth.cmd_auth_register(parsers, environ)


def configure_logging(verbosity):
    """Reconfigure logging with selected verbosity

    Sets the root logger and updates the args so oauth logging
    will also be configured properly

    Args:
        args (Object): Application args
        verbosity (int): The logging veribisty...
            0: WARN
            1: INFO
            >1: DEBUG
    """
    if verbosity <= 0:
        level = logging.WARN
    elif verbosity == 1:
        level = logging.INFO
    else:
        assert verbosity > 1
        level = logging.DEBUG
    logging.basicConfig(level=level)


def ensure_profile_dir_exists(profile_dir):
    """Make sure the profile dir for the command exist

    Args:
        profile_dir (str); The path of the profile dir
    """
    profile_dir = os.path.expanduser(profile_dir)
    if not os.path.exists(profile_dir):
        logger.debug('Creating profile directory: ' + profile_dir)
        os.makedirs(profile_dir)
    logger.debug('Profile directory: ' + profile_dir)


def main(argv=None, environ=None, callback_register_sub_commands=None):
    """Main script entry point for gmailtool
    """
    argv = argv or sys.argv
    environ = environ or os.environ
    callback_register_sub_commands = callback_register_sub_commands or register_sub_commands

    # Get comand line arguments (using the  argparse library)
    args = argparse.Namespace()
    parser = argparse.ArgumentParser(description='Command line tool for fetching messages from your Gmail inbox',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # No-Option arguments
    args.executable = argv[0]
    args.executable_name = os.path.basename(args.executable)

    # Global arguments
    default_profile_dir = environ.get('PROFILE_DIR')
    if default_profile_dir is None:
        assert len(args.executable_name) > 0, 'No profile-dir is specified and executable name is missing or zero length'
        default_profile_dir = '~/.' + args.executable_name
    parser.add_argument('--profile-dir', default=default_profile_dir, help='The directory to store persistant data')
    parser.add_argument('--verbose', '-v', action='count', help='Increase logging verbosity')

    # Command level arguments using subparsers
    sub_parsers = parser.add_subparsers(title='command', help='gmailtool subcommands')
    callback_register_sub_commands(sub_parsers, environ)

    # Parse
    parser.parse_args(argv[1:], namespace=args)

    # Run Initialization Code
    configure_logging(args.verbose)
    ensure_profile_dir_exists(args.profile_dir)

    # Execute sub command
    args.func(args)
