""" GoogleAuthenticator is a wrapper for google_auth_oauthlib.flow and supports
        - console based
        - local server based Google auth

    Prerequisites:
        pip install google_auth_oauthlib

    Read more:
        https://developers.google.com/api-client-library/python/auth/installed-app
"""

__author__ = 'sumeetsarkar4@gmail.com (Sumeet Sarkar)'

from google_auth_oauthlib.flow import InstalledAppFlow


class GoogleAuthenticator:

    def __init__(self, client_id, scopes):
        self.__flow = InstalledAppFlow.from_client_secrets_file(
            client_id, scopes=scopes)

    def initiate(self, config=None):
        if config:
            self.__credentials = self.__flow.run_local_server(
                host=config['host'] or 'localhost',
                port=config['port'] or 9091,
                authorization_prompt_message='Please visit this URL: {url}',
                success_message='The auth flow is complete; you may close this window.',
                open_browser=True)
        else:
            self.__credentials = self.__flow.run_console()

    @property
    def credentials(self):
        return self.__credentials
