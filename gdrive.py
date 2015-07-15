#!/usr/bin/python

import httplib2
import pprint
import csv
import os
import mimetypes
import time

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

from email.mime.text import MIMEText
import base64

SCOPES = 'https://www.googleapis.com/auth/gmail.compose'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Quickstart'

SENDER_EMAIL_ADDRESS = '####################'

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    flags = None
    home_dir = os.path.expanduser('~') + '/dev/stubhub/'
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatability with Python 2.6
            credentials = tools.run(flow, store)
        print ('Storing credentials to ' + credential_path)
    return credentials



def createMessage(sender, to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes())
    raw = raw.decode()
    body = {'raw': raw}

    
    return body

def sendMessage(service, user_id, message):
    message = (service.users().messages().send(userId=user_id, body=message)
               .execute())
    return message

def complete(recipient, subject, seatInfo):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    message = createMessage(SENDER_EMAIL_ADDRESS, recipient, subject, seatInfo)
    sendMessage(service, 'me', message)

def main():

    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    message = createMessage(SENDER_EMAIL_ADDRESS, SENDER_EMAIL_ADDRESS, 'test', 'test-main')
    sendMessage(service, 'me', message)


if __name__ == '__main__':
    main()
