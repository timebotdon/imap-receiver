import mailparser
import imaplib
import json
from pycti import OpenCTIApiClient

# OpenCTI connector credentials
api_url = ''
api_token = ''

# Email credentials
USER = ''
PASS = ''


def importToOCTI(jsonData):
  # OpenCTI API client initialization
  opencti_api_client = OpenCTIApiClient(api_url, api_token)
  # Import the bundle
  opencti_api_client.stix2.import_bundle_from_json(jsonData, update=False)


def getMessageText():
  for i in range(1, total_messages+1, 1):
    #print("msg number:", i)

    # fetch the email message by ID
    res, msg = imap.fetch(str(i), "RFC822")

    for response in msg:
      ## If the response is a "tuple" datatype then..
      if isinstance(response, tuple):
        # parse a bytes email into a message object
        mail = mailparser.parse_from_bytes(response[1])
        msgObject = mail.message
        #print(content_type)

        if msgObject.is_multipart():
          # Walk through each part
          for part in msgObject.walk():
            #Get content type
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))
            #print(content_disposition)

            if content_type == "application/json":
              try:
                attachContent = part.get_payload(decode = True).decode()
                #print(attachContent)
                jsonData = json.loads(attachContent)
                #print(jsonData)
                importToOCTI(attachContent)
                #importToOcti(attachContent) <----- send json data to OCTI here
              except Exception as e:
                print(e)


# create an IMAP4 class with SSL 
imap = imaplib.IMAP4_SSL("imap.gmail.com")

# authenticate
imap.login(USER, PASS)

# Select mail folder
status, messages = imap.select("test")

# Get total number of emails
total_messages = int(messages[0])
#print("Total Mails in INBOX:", total_messages)

# get message content
getMessageText()

imap.close()
imap.logout()