"""Main entry point for gmailtool"""

import logging
import os
import sys
import gmailtool.argument_parser


logger = logging.getLogger('gmailtool')


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
    """Make sure the profile dir for the command exists
    
    Args:
        profile_dir (str); The path of the profile dir
    """
    profile_dir = os.path.expanduser(profile_dir)
    if not os.path.exists(profile_dir):
        logger.debug('Creating profile directory: ' + profile_dir)
        os.makedirs(profile_dir)
    logger.debug('Profile directory: ' + profile_dir)


def main(argv=None, environ=None):
    """Main script entry point for gmailtool
    """

    # Get Arguments
    argv = argv or sys.argv
    environ = environ or os.environ
    args = gmailtool.argument_parser.parse_args(argv, environ)

    # Run Initialization Code
    configure_logging(args.verbose)
    ensure_profile_dir_exists(args.profile_dir)

    # Execute sub command
    args.func(args)

