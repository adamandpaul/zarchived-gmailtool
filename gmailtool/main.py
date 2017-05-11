"""Main entry point for gmailtool"""

import argparse
import sys


def auth(args):
    """The authentication command
    """
    raise NotImplementedError('auth function not implemented')


def cmd_auth_configure_argument_parser(parser):
    """Configure the argument parser for use with the auth command
    
    Args:
        parser (ArguementParser): The arguement parser to configure
    """
    parser.set_defaults(func=auth)



def main(argv=sys.argv):
    """Main script entry point for gmailtool
    """
    parser = argparse.ArgumentParser(description='Command line tool for fetching messages from your Gmail inbox')
    subparsers = parser.add_subparsers(title='command', help='gmailtool subcommand')

    auth_parser = subparsers.add_parser('auth', help='Authenticate and save credentials for future invocations of gmailtool')
    cmd_auth_configure_argument_parser(auth_parser)

    args = parser.parse_args(argv[1:])
    args.func(args)


    



