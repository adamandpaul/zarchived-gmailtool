"""Main entry point for gmailtool"""

import argparse
import logging
import os
import sys

from gmailtool import config

logger = logging.getLogger('gmailtool')

def ensure_profile_dir_exists(profile_dir):
    """Make sure the profile dir for the command exists
    
    Args:
        profile_dir (str); The path of the profile dir
    """
    profile_dir = os.path.expanduser(profile_dir)
    if not os.path.exists(profile_dir):
        logger.debug('Creating profile directory: ' + profile_dir)
        os.makedirs(profile_dir)
    logger.debug('Profile directory: ' + profile_dir)


def configure_logging(verbosity):
    """Configure logging
    
    Args:
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


def parse_args(argv, environ, command_infos):
    """Parse command line and environment variable arguments
    
    Args:
        argv (list of strings): The arguments to parse
        environ (dict): The executable environment variables
        command_infos (list of dicts): A list of dictionaries outlining command information
    
    Returns:
        object: Object with properties of parse executable arguments
    """
    args = argparse.Namespace()
    parser = argparse.ArgumentParser(description='Command line tool for fetching messages from your Gmail inbox',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # No-Option Arguments
    args.executable = argv[0]
    args.executable_name = os.path.basename(args.executable)

    # Global Arguments
    default_profile_dir = environ.get('PROFILE_DIR')
    if default_profile_dir is None:
        assert len(args.executable_name) > 0, 'No profile-dir is specified and executable name is missing or zero length'
        default_profile_dir = '~/.' + args.executable_name
    parser.add_argument('--profile-dir', default=default_profile_dir, help='The directory to store persistant data')
    parser.add_argument('--verbose', '-v', action='count', help='Increase logging verbosity')

    # Command Level Arguments
    sub_parsers = parser.add_subparsers(title='command', help='gmailtool subcommands')
    for command_info in command_infos:
        sub_parser = sub_parsers.add_parser(command_info['command'], help=command_info['help'])
        command_info['register_function'](sub_parser, environ)

    # Parse and Return
    parser.parse_args(argv[1:], namespace=args)
    return args


def main(argv=None, environ=None, command_infos=None):
    """Main script entry point for gmailtool
    """
    argv = argv or sys.argv
    environ = environ or os.environ
    command_infos = command_infos or config.command_infos
    args = parse_args(argv, environ, command_infos)
    configure_logging(args.verbose)
    ensure_profile_dir_exists(args.profile_dir)
    args.func(args)

