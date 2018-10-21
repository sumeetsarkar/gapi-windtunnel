"""Python gmail client

Usage:
  $ python main.py
"""

# pip install --upgrade google-api-python-client
# pip install google_auth_oauthlib

__author__ = 'sumeetsarkar4@gmail.com (Sumeet Sarkar)'

import sys

from libgoogle.auth import GoogleAuthenticator
from libgoogle import GmailService


class GoogleAPIClient:

  def __init__(self, clientIdPath, scopes):
    self.__clientIdPath = clientIdPath
    self.__scopes = scopes
    self.__googleAuth = None
    self.__gmailService = None
  

  def authenticate(self, config):
    self.__googleAuth = GoogleAuthenticator(self.__clientIdPath, self.__scopes)
    self.__googleAuth.initiate(config)
    return self


  def prepare_service(self, serviceName):
    if self.__googleAuth is None or self.__googleAuth.credentials is None:
      raise Exception('API Client not yet authenticated')
    if serviceName == 'gmail':
      if self.__gmailService is None:
        self.__gmailService = GmailService(self.__googleAuth)
      return self.__gmailService


def scrape_daily_coding_problem(apiClient, argv):
  service = apiClient.prepare_service('gmail')
  messages = service.list_messages_matching_query(
    user_id='me',
    query='from:founders@dailycodingproblem.com',
    limit=5,
  )
  print('\n\nFound {} messages...\n\n'.format(len(messages)))
  print('--------------------------------------------------------------------------')
  begStringLen = len('Good morning! Here\'s your coding interview problem for today.')
  endString = 'Upgrade to premium'
  for m in messages:
    message = service.get_mime_message('me', m['id'])
    indexEnd = message.index(endString)
    print(message[int(begStringLen) : int(indexEnd)])
    print('--------------------------------------------------------------------------')


def main(argv):
  scopes = [
    'https://mail.google.com/',
    'https://www.googleapis.com/auth/gmail.readonly',
  ]
  apiClient = GoogleAPIClient('client_id.json', scopes)
  apiClient.authenticate({
      'host': 'localhost',
      'port': 9091,
    })
  scrape_daily_coding_problem(apiClient, argv)


if __name__ == '__main__':
  try:
    main(sys.argv)
  except Exception as e:
    print(e)
