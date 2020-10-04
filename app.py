import mailparser
import imaplib
import json
import base64
import re
from pycti import OpenCTIApiClient

# OpenCTI connector credentials
api_url = ''
api_token = ''

# Email configuration
email_imapserver = 'imap.gmail.com' # Imap server address/domain name
email_folder = 'test' # Target folder to ingest mail from
email_username = ''
email_password = ''


def importToOCTI(jsonData):
  # OpenCTI API client initialization
  opencti_api_client = OpenCTIApiClient(api_url, api_token)
  # Import the bundle
  opencti_api_client.stix2.import_bundle_from_json(jsonData, update=True)

def getMessageText():
  for i in range(1, total_messages+1, 1):

    # fetch the email message by ID
    res, msg = imap.fetch(str(i), "RFC822")

    for response in msg:
      ## If the response is a "tuple" datatype then..
      if isinstance(response, tuple):
        # parse a bytes email into a message object
        mail = mailparser.parse_from_bytes(response[1])
        msgAttachContentType = mail.attachments[0]["mail_content_type"]
        attachmentFilename = mail.attachments[0]["filename"]
        
        filenameConventionReg = 'SINGCERT_\d\d-\d\d-\d\d.json' #change naming convention regex here

        # If a json file is found as an attachment and matches naming convention, decode content and upload to opencti.
        if msgAttachContentType == "application/json" and (re.search(filenameConventionReg, attachmentFilename)):
          try:
            msgAttachPayload = base64.b64decode(mail.attachments[0]["payload"]).decode('utf-8')
            importToOCTI(msgAttachPayload)
          except Exception as error:
            print(error)


# create an IMAP4 class with SSL 
imap = imaplib.IMAP4_SSL(email_imapserver)

# authenticate
imap.login(email_username, email_password)

# Select mail folder
status, messages = imap.select(email_folder)

# Get total number of emails
total_messages = int(messages[0])
print("Total Mails in folder:", total_messages)

# get message content
getMessageText()

imap.close()
imap.logout()