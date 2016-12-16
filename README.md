python-gmail-api
================

Connect to the Gmail API using Python.

Only works for sending at the moment, but I do plan to add other functionality eventually.

# https://github.com/chris-brown-nz/python-gmail-api
# Created: 2016-12-14
# Author: Chris Brown
# Based on and using code from examples at: https://developers.google.com/gmail/api/
# Google API test harness: https://developers.google.com/apis-explorer/?hl=en_GB#p/gmail/v1/

Install
-------

This is a step-by-step guide on how to get a message sender going (note this is for Python 3.5):
Install requirements ($ pip3??? requirements.txt)
google-api-python-client == 1.5.5
Go to Google APIs: https://console.developers.google.com/iam-admin/projects
Go Project > Create project
Give the project a name and wait for Google to create the project
From the list of APIs in the library, select 'Gmail API' and on the next screen click 'Enable'
On the left-hand side, click 'Credentials'
Click Create credentials > OAuth client ID
Click 'Configure consent screen'
Enter a Product Name and click save
Under 'client ID' choose other. I'm not sure what this is for, I used my project name
Click 'OK' to get rid of the popup
Click the download icon and save the file to somewhere in your project - rename it, e.g. 'python_gmail_api_client_secret.json'
Add the code to your project.
Modify the following as required:
CLIENT_SECRET_FILE
APPLICATION_NAME
MANUAL_AUTH
The first time you call the code, you will be asked to go to a URL and after authenticating, copy the auth code into terminal

Usage:

Call script python_gmail_api.py ($ python3 python_gmail_api.pg) directly to send an email from a CLI.

Import PythonGmailAPI
PythonGmailAPI().gmail_send(sender_address, to_address, subject, body)

The following API test harness is useful for troubleshooting: https://developers.google.com/apis-explorer/?hl=en_GB#p/gmail/v1/