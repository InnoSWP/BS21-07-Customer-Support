import googleapiclient
import httplib2
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build

CREDENTIALS_FILE = 'creds.json'
spreadsheet_id = '1PwgkG6nqIQqj7KiXRv19Hcy0igg9EfS6kkG2gfVDgzI'

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = googleapiclient.discovery.build('sheets', 'v4', http = httpAuth)

# Read first 100 answers and corresponding questions.
# Returns in format [[question1, answer1], [question2, answer2], ...]
def sheetRead():
    values = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range='A1:B100',
        majorDimension='ROWS'
    ).execute()
    return values['values']

# Find the number of current written questions
def sheetRows():
    values = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range='A1:B100',
        majorDimension='ROWS'
    ).execute()
    return len(values['values'])

# Write in the B column
def sheetWriteAnswer(number, answer):
    number
    number += 1
    writeRange = "B" + str(number) + ":" + "B" + str(number)
    values = service.spreadsheets().values().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={
            "valueInputOption": "USER_ENTERED",
            "data": [
                {"range": writeRange,
                "majorDimension": "ROWS",
                "values": [[answer]]},
	    ]
        }

    ).execute()

# Write in the A column
def sheetWriteQuestion (number, question):
    number += 1
    writeRange = "A" + str(number) + ":" + "A" + str(number)
    values = service.spreadsheets().values().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={
            "valueInputOption": "USER_ENTERED",
            "data": [
                {"range": writeRange,
                "majorDimension": "ROWS",
                "values": [[question]]},
	    ]
        }

    ).execute()

def sheetReadFirst():
    values = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range='A1:A1',
        majorDimension='ROWS'
    ).execute()
    return values['values']

def sheetReadG1():
    values = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range='G1:G1',
        majorDimension='ROWS'
    ).execute()
    return values['values']


def sheetWriteSmth(smth):
    writeRange = "G1:G1"
    values = service.spreadsheets().values().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={
            "valueInputOption": "USER_ENTERED",
            "data": [
                {"range": writeRange,
                 "majorDimension": "ROWS",
                 "values": [[smth]]},
            ]
        }
    ).execute()
    return sheetReadG1()