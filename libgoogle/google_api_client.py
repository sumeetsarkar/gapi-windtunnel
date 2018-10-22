""" GoogleAPIClient is a wrapper client for multitude of Google APIs, currently supporting
        - Authentication using GoogleAuthenticator
        - GmailService
"""

__author__ = 'sumeetsarkar4@gmail.com (Sumeet Sarkar)'

import sys

from .auth import GoogleAuthenticator
from .gmail_service import GmailService


class GoogleAPIClient:
    SERVICE_GMAIL = 'gmail'

    def __init__(self, client_id, scopes):
        self.__googleAuth = GoogleAuthenticator(
            client_id, scopes)
        self.__gmailService = None

    def authenticate(self, config=None):
        self.__googleAuth.initiate(config)
        return self

    def prepare_service(self, serviceName):
        if self.__googleAuth is None or self.__googleAuth.credentials is None:
            raise Exception('API Client not yet authenticated')
        if serviceName == GoogleAPIClient.SERVICE_GMAIL:
            if self.__gmailService is None:
                self.__gmailService = GmailService(self.__googleAuth)
            return self.__gmailService

