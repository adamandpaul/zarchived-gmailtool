"""Release Level Configuration
"""

import gmailtool.auth

command_infos = [
    {
        'command': 'auth',
        'help': 'Authenticate and save credentials for future invocations of gmailtool',
        'register_function': gmailtool.auth.cmd_auth_register,
    },
]
