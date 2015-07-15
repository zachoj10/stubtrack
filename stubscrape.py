import argparse
from bs4 import BeautifulSoup
import requests
from requests.auth import HTTPBasicAuth
import time
import os
from datetime import datetime
import sys

from gdrive import complete


parser = argparse.ArgumentParser(
        description='Upload a list of state data to the database')
parser.add_argument('-e', '--event', action='store',
                    type=int, help='event id to search for', required=True)
parser.add_argument('-p', '--price', action='store',
                    type=int, help='max price searching for')
parser.add_argument('-s', '--section', nargs='+', action='store',
                    type=str, help='max price searching for')

STUB_API_CONNECT_SECRET = os.environ.get('STUB_API_CONNECT_SECRET', '')
STUB_API_CONNECT_CONSUMER = os.environ.get('STUB_API_CONNECT_CONSUMER', '')

STUB_USER = os.environ.get('STUB_USER', '')
STUB_PASS = os.environ.get('STUB_PASS', '')

DEST_EMAIL_ADDRESS = 'zjosephson@gmail.com'

args = parser.parse_args()

eventid = args.event
maxPrice = args.price
sections = args.section

s = requests.Session()
url = "https://api.stubhub.com/login"


data = 'grant_type=password&username={0}&password={1}'.format(STUB_USER, STUB_PASS)
r = s.post(url, auth=HTTPBasicAuth(STUB_API_CONNECT_CONSUMER, STUB_API_CONNECT_SECRET), data = data)
if r.status_code != 200:
    sys.exit('ERROR: Unable to authenticate')


data = r.json()
token = data['access_token']

headers = {'Authorization': 'Bearer {0}'.format(token)}

foundTickets = []

page = s.get('https://api.stubhub.com/catalog/events/v2/{0}'.format(eventid),  headers=headers)
soup = BeautifulSoup(page.text, 'html.parser')
title = soup.find('title').text
eventTimeString = soup.find('eventdateutc').text
eventDate = datetime.strptime(eventTimeString, '%Y-%m-%dT%H:%M:%SZ')


while eventDate > datetime.utcnow():
    count = -1
    start = 0

    while(count == -1 or count > start):
        page = s.get('https://api.stubhub.com/search/inventory/v1?eventid={0}&start={1}&rows={2}&pricemax={3}'.format(eventid, start, start + 200, maxPrice),  headers=headers)
        start += 200
        #print(page.text)
        tickets = page.json()
        count = int(tickets['totalListings'])

        for item in tickets['listing']:
            #print(item)
            section = item['sectionName']
            cost = '{0:,.2f}'.format(item['currentPrice']['amount'])
            itemID = tuple((section, cost, item['row'], item['seatNumbers']))
            freq = 2500
            dur = 500
            if sections and section in sections and not itemID in foundTickets:
                displayString = 'Section: {0} Row: {1} Current price: ${2}'.format(section, item['row'], cost)
                print(displayString)
                foundTickets.append(itemID)
                complete(DEST_EMAIL_ADDRESS, title, displayString)
            elif not sections and not itemID in foundTickets:
                displayString = 'Section: {0} Row: {1} Current price: ${2}'.format(section, item['row'], cost)
                print(displayString)
                foundTickets.append(itemID)
                complete(DEST_EMAIL_ADDRESS, title, displayString)
    time.sleep(6)



