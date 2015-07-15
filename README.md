README.md

# StubHub Seat/Price Monitor

This is a simple python script designed to monitor the price and avaliability of seats at a single event that is listed on stubhub.com. If the desired seat constraints are met, the user will be notified via an email sent using the Gmail API. 

# Requirements 
- beautifulsoup4==4.4.0
- google-api-python-client==1.4.1
- httplib2==0.9.1
- oauth2client==1.4.12
- pyasn1==0.1.8
- pyasn1-modules==0.0.6
- requests==2.7.0
- rsa==3.1.4
- simplejson==3.7.3
- six==1.9.0
- uritemplate==0.6

# Configuration Instructions
1. Register for Google API here: (https://console.developers.google.com "https://console.developers.google.com")
    - Create a new project and enable the Gmail API
    - Create a set of credentials and download JSON of the credentials.
    - Rename JSON download to 'client_secret.json' and place in local project directory

2. Register for Stubhub API here: (https://developer.stubhub.com/store/ "https://developer.stubhub.com/store/")
    - Create a new application
    - Create a set of Production Keys
    - (RECOMENDED) Store production keys as well as stubhub login information as environment variables in virtual environment with variable names 'STUB_API_CONNECT_SECRET', 'STUB_API_CONNECT_CONSUMER', 'STUB_USER', 'STUB_PASS' (RECOMENDED)

3. Set variable in stubscrape.py to personal preferences
    - DEST_EMAIL_ADDRESS : Email address that will recieve ticket notification

4. Set variable in gdrive.py to person preferences
    - SENDER_EMAIL_ADDRESS : Gmail address that is sending ticket notifications