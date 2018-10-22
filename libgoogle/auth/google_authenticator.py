"""
"""

# pip install google_auth_oauthlib

__author__ = 'sumeetsarkar4@gmail.com (Sumeet Sarkar)'

from google_auth_oauthlib.flow import InstalledAppFlow


class GoogleAuthenticator:

    def __init__(self, clientIdPath, scopes):
        self.__clientIdPath = clientIdPath
        self.__scopes = scopes
        self.__flow = InstalledAppFlow.from_client_secrets_file(
            clientIdPath, scopes=scopes)

    def initiate(self, mode=None):
        if mode:
            self.__credentials = self.__flow.run_local_server(
                host=mode['host'] or 'localhost',
                port=mode['port'] or 9091,
                authorization_prompt_message='Please visit this URL: {url}',
                success_message='The auth flow is complete; you may close this window.',
                open_browser=True)
        else:
            self.__credentials = self.__flow.run_console()

    @property
    def credentials(self):
        return self.__credentials
