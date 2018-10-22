> GAPI Playground in python

### Initialize the GAPI Client and Authenticate
```python
    client_id = 'client_id.json'
    # List the scopes for OAuth2.0 authorization
    scopes = [
        'https://mail.google.com/',
        'https://www.googleapis.com/auth/gmail.readonly',
    ]

    # Initialize API Client
    api_client = GoogleAPIClient(client_id, scopes)

    # Authenticate with local server
    api_client.authenticate({
        'host': 'localhost',
        'port': 9091,
    })

    # Or
    # Authenticate with terminal
    api_client.authenticate()
```


### Prepare the Gmail service
```python
    gmail_service = api_client.prepare_service(GoogleAPIClient.SERVICE_GMAIL)
```

### Search for Gmail Messages
```python
    messages = service.list_messages_matching_query(
        user_id='me',
        query='from:founders@dailycodingproblem.com',
        limit=5,
    )
```

### Get MIME message by Id
```python
    for m in messages:
        email = service.get_mime_message('me', m['id'])
```