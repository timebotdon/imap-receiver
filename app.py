import os
import email
from email.header import decode_header
import imaplib
import html2text
import json

# account credentials
USER = ''
PASS = ''

""" 
# output
OUTPUT = "out"

## TESTING only. save to local disk
def writeToFile(filename, msgobject):
  name = filename.replace(":", "-").strip()
  print(name)
  filename = name + ".json"
  filepath = os.path.join("out", filename)
  open(filepath, "w").write(msgobject)
 """

def convertToJSON(msgsubject, msgdate, msgfrom, msgbody):
  # a Python object (dict):
  msgobject = {
    "subject": msgsubject,
    "date": msgdate,
    "from": msgfrom,
    #"to": msgto,
    #"cc": msgcc,
    #"bcc": msgbcc,
    "body": msgbody
  }
  
  y = json.dumps(msgobject)
  #writeToFile(msgobject["subject"], msgobject)
  #print(msgobject["subject"])

  print(y)


#if not isinstance(text, unicode):
#  text = unicode(text, "utf-8")


def getMessageText(msgObjects):
  for i in range(messages, messages-3, -1):
    #print("msg number:", i)

    # fetch the email message by ID
    res, msg = imap.fetch(str(i), "RFC822")

    for response in msg:
      ## If the response is a "tuple" datatype then..
      if isinstance(response, tuple):
        # parse a bytes email into a message object
        msg = email.message_from_bytes(response[1])
        #print(dir(msg))

        msgdate = msg.get("Date")
        msgfrom = msg.get("From")
        msgsubject = decode_header(msg["Subject"])[0][0]

        if isinstance(msgsubject, bytes):
          msgsubject = msgsubject.decode()

        # If message object is multipart
        if msg.is_multipart():

          # Walk through each part
          for part in msg.walk():

            #Get content type
            content_type = part.get_content_type()
            # print("Type:",content_type)
            content_disposition = str(part.get("Content-Disposition"))
            try:
              msgbody = part.get_payload(decode = True).decode()
            except:
              pass
            
            if content_type == "text/plain" and "attachment" not in content_disposition:
              #msgbody = msgbody
              pass  
            
        
        else:
          content_type = msg.get_content_type()
          # print("Type:",content_type)
          msgbody = msg.get_payload(decode=True).decode()
          if content_type == "text/plain":
            msgbody = msgbody
            #print(body)
            pass
        
        if content_type == "text/html":
          # if it's HTML, create a new HTML file and open it in browser
          h2t = html2text.HTML2Text()
          
          ## html2text OPTIONS
          h2t.single_line_break = True
          h2t.ignore_links = True
          h2t.ignore_tables = True
          h2t.ignore_images = True
          h2t.ignore_anchors = True
          
          text = h2t.handle(msgbody)
          msgbody = text

          convertToJSON(msgsubject, msgdate, msgfrom, msgbody)

    #finalData = [msgsubject, msgdate, msgfrom, msgbody]
    #print(finalData)
    #return finalData
    #convertToJSON(finalData)

""" 
if not os.path.isdir(OUTPUT):
  os.mkdir(OUTPUT)
 """

# create an IMAP4 class with SSL 
imap = imaplib.IMAP4_SSL("imap.gmail.com")

# authenticate
imap.login(USER, PASS)

# Select mail folder
status, messages = imap.select("INBOX")

# Get total number of emails
messages = int(messages[0])

print("Total Mails in INBOX:", messages)

# get message content
getMessageText(messages)

imap.close()
imap.logout()