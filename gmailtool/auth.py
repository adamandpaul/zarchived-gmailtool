# -*- coding: utf-8 -*-
"""Google Authentication Handling"""

import json
import logging
import os
import tempfile

from gmailtool import config

import oauth2client
import oauth2client.file
import oauth2client.tools

logger = logging.getLogger('gmailtool.auth')


def cmd_auth(args):
    """The authentication command
    """
    logger.debug('Running command auth')

    credentials_storage_path = os.path.join(args.profile_dir, config.oauth_credentials_storage_filename)
    credentials_storage = oauth2client.file.Storage(credentials_storage_path)
    credentials = credentials_storage.get()
    if credentials is None or credentials.invalid:


        client_secret_file_handle, client_secret_path = tempfile.mkstemp()
        client_secret_fout = os.fdopen(client_secret_file_handle, 'w')
        json.dump(config.oauth_client_secret, client_secret_fout)
        client_secret_fout.close()
        flow = oauth2client.client.flow_from_clientsecrets(client_secret_path,
                                                           config.oauth_scopes)
        flow.user_agent = config.oauth_application_name
        credentials = oauth2client.tools.run_flow(flow, credentials_storage, args)
        os.remove(client_secret_path)

    return credentials


def cmd_auth_register(parsers, environ):
    """Configure the argument parser for use with the auth command
    
    Args:
        parsers (Parsers): The parsers which belong to the higher level parser
    """
    parser = parsers.add_parser('auth',
                                help='Authenticate and save credentials for future invocations of gmailtool',
                                parents=[oauth2client.tools.argparser])
    parser.set_defaults(func=cmd_auth)

