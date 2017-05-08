"""Main entry point for gmailtool"""

import argparse
import sys


def auth(args):
    """The authentication command
    """
    pass



def main(argv=sys.argv):
    """Main script entry point for gmailtool
    """

    parser = argparse.ArgumentParser(description='Command line tool for fetching messages from your Gmail inbox')
    parser.add_argument('command')
    args = parser.parse_args(argv[1:])

    if args.command == 'auth':
        import pdb; pdb.set_trace()
    else:
        raise Exception('Unknown command: ' + args.command)

    



