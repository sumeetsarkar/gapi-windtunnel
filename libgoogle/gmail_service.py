""" GmailService supports
        - listing messages based on query  
        - getting message details

    Prerequisites
        pip install google-api-python-client

    API Reference
        https://developers.google.com/gmail/api/v1/reference/
"""

__author__ = 'sumeetsarkar4@gmail.com (Sumeet Sarkar)'

import base64
import email
import json
import sys

from googleapiclient.discovery import build
from apiclient import errors


class GmailService:

    API_SERVICE_NAME = 'gmail'
    API_VERSION = 'v1'

    def __init__(self, authenticator):
        self.__service = build(
            GmailService.API_SERVICE_NAME,
            GmailService.API_VERSION,
            credentials=authenticator.credentials)

    def list_messages_matching_query(self, user_id, query='', limit=sys.maxsize):
        """List all Messages of the user's mailbox matching the query.

        Args:
          user_id: User's email address. The special value "me"
          can be used to indicate the authenticated user.
          query: String used to filter messages returned.
          Eg.- 'from:user@some_domain.com' for Messages from a particular sender.

        Returns:
          List of Messages that match the criteria of the query. Note that the
          returned list contains Message IDs, you must use get with the
          appropriate ID to get the details of a Message.
        """
        try:
            response = self.__service.users().messages().list(userId=user_id,
                                                              q=query).execute()
            messages = []
            if 'messages' in response:
                messages.extend(response['messages'])

            if len(messages) > limit:
                messages = messages[0:limit]

            while 'nextPageToken' in response and len(messages) <= limit:
                page_token = response['nextPageToken']
                response = self.__service.users().messages().list(userId=user_id, q=query,
                                                                  pageToken=page_token).execute()
                messages.extend(response['messages'])
            return messages
        except errors.HttpError as error:
            print('An error occurred: %s' % error)

    def get_message(self, user_id, msg_id):
        """Get a Message with given ID.

        Args:
          service: Authorized Gmail API service instance.
          user_id: User's email address. The special value "me"
          can be used to indicate the authenticated user.
          msg_id: The ID of the Message required.

        Returns:
          A Message.
        """
        try:
            message = self.__service.users().messages().get(
                userId=user_id, id=msg_id).execute()

            # print('Message snippet: %s' % message['snippet'])

            return message
        except errors.HttpError as error:
            print('An error occurred: %s' % error)

    def get_mime_message(self, user_id, msg_id):
        """Get a Message and use it to create a MIME Message.

        Args:
          service: Authorized Gmail API service instance.
          user_id: User's email address. The special value "me"
          can be used to indicate the authenticated user.
          msg_id: The ID of the Message required.

        Returns:
          A MIME Message, consisting of data from Message.
        """
        try:
            message = self.__service.users().messages().get(userId=user_id, id=msg_id,
                                                            format='raw').execute()
            mytext = ''
            msg_str = base64.urlsafe_b64decode(
                message['raw'].encode('ASCII')).decode('UTF-8')
            mime_msg = email.message_from_string(msg_str)
            for parts in mime_msg.walk():
                mime_msg.get_payload()
                if parts.get_content_type() == 'text/plain':
                    mytext += parts.get_payload()

        except errors.HttpError as error:
            print('An error occurred: %s' % error)
        return mytext
