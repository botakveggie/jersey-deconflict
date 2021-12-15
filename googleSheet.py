from __future__ import print_function
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow, Flow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from credentials import *


CLIENT_SECRET_FILE = client_secret_file

API_NAME = "sheets"
API_VERSION = "v4"

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = sheet_id
SAMPLE_RANGE_NAME = sheet_range

def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                client_secret_file, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build(API_NAME, API_VERSION, credentials=creds)

    sheet_metadata = service.spreadsheets().get(spreadsheetId=SAMPLE_SPREADSHEET_ID).execute()
    list_of_sheets  = sheet_metadata.get('sheets')
    # print(len(list(list_of_sheets)))
    list_of_titles = []
    for  item in list_of_sheets:
        title = (item.get("properties").get('title'))
        list_of_titles.append(title)
    print (list_of_titles)
    

#   Getting spreadsheet.values()
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    jersey_choices = {}
    conflict = []
    
    if not values:
        print('No data found.')
    else:
        for row in values:
            name, choice = row[NAME_COL], row[CHOICE_COL]
            if choice not in jersey_choices.keys():
                jersey_choices[choice] = [name]
            else:
                jersey_choices[choice].append(name)
                if choice not in conflict:
                    conflict.append(choice)
            
            # print('%s, %s' % (row[0], row[4]))
#     # Name, Size, Year, 1stChoice, 2ndChoice, 3rdChoice
    print("conflicted jersey numbers are %s" % conflict)
    
    need_to_change = []
    for num in conflict:
        need_to_change += jersey_choices[num]
    print("please check jersey num for the following \n" + str(need_to_change))
    

if __name__ == '__main__':
    main()