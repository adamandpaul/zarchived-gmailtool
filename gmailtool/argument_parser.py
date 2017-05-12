"""Module to registering commands and configuring argparsers
"""

import argparse
import logging
import os
import oauth2client.tools


logger = logging.getLogger('gmailtool.argparse')


def register_sub_commands(parsers, environ):
    """Register sub commands
    
    This function calls the register commands fucntion associated with
    each sub command.
    
    Args:
        parsers (Arguement Parsers Object): Object to use to add parsers for commands
        environ (dict): The environment dictionary
    """
    import gmailtool.auth
    gmailtool.auth.cmd_auth_register(parsers, environ)


def parse_args(argv, environ):
    """Parse command line and environment variable arguments
    
    Args:
        argv (list of strings): The arguments to parse
        environ (dict): The executable environment variables
    
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
    register_sub_commands(sub_parsers, environ)

    # Parse and Return
    parser.parse_args(argv[1:], namespace=args)
    return args

