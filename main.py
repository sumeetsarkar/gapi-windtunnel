""" Scrapes Daily Coding Problems from Gmail messages

    Prerequisites:
        pip install google-api-python-client
        pip install google_auth_oauthlib

    Usage:
        $ python main.py
"""


__author__ = 'sumeetsarkar4@gmail.com (Sumeet Sarkar)'

import sys

from libgoogle import GoogleAPIClient


def scrape_daily_coding_problem(service, argv):
    messages = service.list_messages_matching_query(
        user_id='me',
        query='from:founders@dailycodingproblem.com',
        limit=5,
    )
    print('\n\nFound {} messages...\n\n'.format(len(messages)))
    print('--------------------------------------------------------------------------')
    beg_string_len = len(
        'Good morning! Here\'s your coding interview problem for today.')
    end_string = 'Upgrade to premium'
    for m in messages:
        message = service.get_mime_message('me', m['id'])
        end_index = message.index(end_string)
        print(message[int(beg_string_len): int(end_index)])
        print('--------------------------------------------------------------------------')


def main(argv):
    # Obtain client_id.json from Google API Console
    # Please do not commit client_id.json
    client_id = 'client_id.json'
    # List the scopes for OAuth2.0 authorization
    scopes = [
        'https://mail.google.com/',
        'https://www.googleapis.com/auth/gmail.readonly',
    ]
    # Initialize API Client
    api_client = GoogleAPIClient(client_id, scopes)
    # Authenticate
    api_client.authenticate({
        'host': 'localhost',
        'port': 9091,
    })
    # Prepare the gmail service
    gmail_service = api_client.prepare_service(GoogleAPIClient.SERVICE_GMAIL)
    # Sample use case of scraping daily coding problems
    scrape_daily_coding_problem(gmail_service, argv)


if __name__ == '__main__':
    try:
        main(sys.argv)
    except Exception as e:
        print(e)
