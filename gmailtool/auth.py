"""Google Authentication Handling"""


def auth(args):
    """The authentication command
    """
    raise NotImplementedError('auth function not implemented')


def cmd_auth_register(parser, environ):
    """Configure the argument parser for use with the auth command
    
    Args:
        parser (ArguementParser): The argument parser to configure
    """
    parser.set_defaults(func=auth)
