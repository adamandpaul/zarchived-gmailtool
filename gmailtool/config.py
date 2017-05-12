"""Release Level Configuration
"""

oauth_application_name = 'gmailtool'

oauth_client_secret = {
    "installed": {
        "client_id": "112272676137-3ijeet0qkkgctotcbj1nc100l3roal29.apps.googleusercontent.com",
        "project_id": "non-billable",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://accounts.google.com/o/oauth2/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_secret": "yrD6BRFRUaKsuQMT26spEGZp","redirect_uris": ["urn:ietf:wg:oauth:2.0:oob", "http://localhost"]
    }
}

oauth_scopes = ['https://www.googleapis.com/auth/gmail.readonly']

oauth_credentials_storage_filename =  'credentials.json'
