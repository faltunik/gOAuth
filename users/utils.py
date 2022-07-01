import os
import google_auth_oauthlib.flow

credentials = {
    "web":
        {
            "client_id": os.environ['CLIENT_ID'],
            "project_id":os.enivron['PROJECT_ID'],
            "auth_uri": os.environ['AUTH_URI'],
            "token_uri": os.environ['TOKEN_URI'],
            "auth_provider_x509_cert_url": os.environ['AUTH_PROVIDER_X509_CERT_URL'],
            "client_secret": os.environ['CLIENT_SECRET'],
            "redirect_uris": [os.environ['REDIRECT_URI']]
        }
        }

def client(state=None):
    scopes = ['https://www.googleapis.com/auth/calendar']
    return google_auth_oauthlib.flow.Flow.from_client_secrets_file(credentials, scopes=scopes, state=state)