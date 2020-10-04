OpenCTI import tool to extract and parse json data forom email attachments.

## Installation
Installation of 3rd party modules is required.
* `pip install html2text`
* `pip install mailparser`
* `pip install pycti`

## Libs required
* mailparser
* imaplib
* json
* pycti

## Testing
* Update `USER` and `PASS` with gmail credentials.
* Update `api_url` and `api_token` with opencti platform URL/Token
* Run: `python app.py`