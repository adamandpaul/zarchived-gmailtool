"""Google Authentication Handling"""

import logging
logger = logging.getLogger('gmailtool.auth')


def cmd_auth(args):
    """The authentication command
    """
    logger.debug('Running command auth')
    raise NotImplementedError('auth function not implemented')


def cmd_auth_register(parser, environ):
    """Configure the argument parser for use with the auth command
    
    Args:
        parser (ArguementParser): The argument parser to configure
    """
    parser.set_defaults(func=cmd_auth)
