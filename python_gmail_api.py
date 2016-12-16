# https://github.com/chris-brown-nz/python-gmail-api
# Created: 2016-12-14
# Author: Chris Brown
# Based on and using code from examples at: https://developers.google.com/gmail/api/
# Google API test harness: https://developers.google.com/apis-explorer/?hl=en_GB#p/gmail/v1/

from __future__ import print_function
import base64
import email.mime.text
import os
import httplib2
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from googleapiclient.discovery import build

# --------------------------------------------------------------------------------------
# This is the name of the secret file you download from https://console.developers.google.com/iam-admin/projects
# Give it a name that is unique to this project
CLIENT_SECRET_FILE = 'python_gmail_api_client_secret.json'
# This is the file that will be created in ~/.credentials holding your credentials. It will be created automatically
# the first time you authenticate and will mean you don't have to re-authenticate each time you connect to the API.
# Give it a name that is unique to this project
CREDENTIAL_FILE = 'python_gmail_api_credentials.json'

APPLICATION_NAME = 'python-gmail-api'
# Set to True if you want to authenticate manually by visiting a given URL and supplying the returned code
# instead of being redirected to a browser. Useful if you're working on a server with no browser.
# Set to False if you want to authenticate via browser redirect.
MANUAL_AUTH = True
# --------------------------------------------------------------------------------------

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
    if MANUAL_AUTH:
        flags.noauth_local_webserver=True
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials at ~/.credentials/gmail-python-quickstart.json
SCOPES = ['https://mail.google.com/',
          'https://www.googleapis.com/auth/gmail.compose',
          'https://www.googleapis.com/auth/gmail.modify',
          'https://www.googleapis.com/auth/gmail.send']

class PythonGmailAPI:
    def __init__(self):
        pass

    def gmail_send(self, sender_address, to_address, subject, body):
        print('Sending message, please wait...')
        message = self.__create_message(sender_address, to_address, subject, body)
        credentials = self.__get_credentials()
        service = self.__build_service(credentials)
        raw = message['raw']
        raw_decoded = raw.decode("utf-8")
        message = {'raw': raw_decoded}
        message_id = self.__send_message(service, 'me', message)
        print('Message sent. Message ID: ' + message_id)


    def __get_credentials(self):
        """Gets valid user credentials from storage.
        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.
        Returns:
            Credentials, the obtained credential.
        """
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir, CREDENTIAL_FILE)
        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            credentials = tools.run_flow(flow, store, flags)
            print('Storing credentials to ' + credential_path)
        return credentials

    def __create_message(self, sender, to, subject, message_text):
      """Create a message for an email.
      Args:
        sender: Email address of the sender.
        to: Email address of the receiver.
        subject: The subject of the email message.
        message_text: The text of the email message.
      Returns:
        An object containing a base64url encoded email object.
      """
      message = email.mime.text.MIMEText(message_text, 'plain', 'utf-8')
      message['to'] = to
      message['from'] = sender
      message['subject'] = subject
      encoded_message = {'raw': base64.urlsafe_b64encode(message.as_bytes())}
      return encoded_message

    ''' SECTION NOT WORKING YET
    def __create_message_with_attachment(self, sender, to, subject, message_text, file):
      message = email.mime.multipart.MIMEMultipart()
      message['to'] = to
      message['from'] = sender
      message['subject'] = subject
      msg = email.mime.text.MIMEText(message_text)
      message.attach(msg)
      content_type, encoding = mimetypes.guess_type(file)
      if content_type is None or encoding is not None:
        content_type = 'application/octet-stream'
      main_type, sub_type = content_type.split('/', 1)
      if main_type == 'text':
        fp = open(file, 'rb')
        msg = email.mime.text.MIMEText(fp.read(), _subtype=sub_type)
        fp.close()
      elif main_type == 'image':
        fp = open(file, 'rb')
        msg = email.mime.image.MIMEImage(fp.read(), _subtype=sub_type)
        fp.close()
      elif main_type == 'audio':
        fp = open(file, 'rb')
        msg = email.mime.audio.MIMEAudio(fp.read(), _subtype=sub_type)
        fp.close()
      else:
        fp = open(file, 'rb')
        msg = email.mime.base.MIMEBase(main_type, sub_type)
        msg.set_payload(fp.read())
        fp.close()
      filename = os.path.basename(file)
      msg.add_header('Content-Disposition', 'attachment', filename=filename)
      message.attach(msg)
      return {'raw': base64.urlsafe_b64encode(message.as_string())}
    '''

    def __send_message(self, service, user_id, message):
      """Send an email message.
      Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        message: Message to be sent.
      Returns:
        Sent Message ID.
      """
      message = (service.users().messages().send(userId=user_id, body=message)
                .execute())
      return message['id']

    def __build_service(self, credentials):
        """Build a Gmail service object.
        Args:
            credentials: OAuth 2.0 credentials.
        Returns:
            Gmail service object.
        """
        http = httplib2.Http()
        http = credentials.authorize(http)
        return build('gmail', 'v1', http=http)

def main():
    sender_address = input('Sender address: ')
    to_address = input('To address: ')
    subject = input('Subject: ')
    body = input('Body: ')
    PythonGmailAPI().gmail_send(sender_address, to_address, subject, body)

if __name__ == '__main__':
    main()

