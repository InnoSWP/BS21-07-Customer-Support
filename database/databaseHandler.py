
import apiclient
import httplib2
from oauth2client.service_account import ServiceAccountCredentials

# Файл, полученный в Google Developer Console
CREDENTIALS_FILE = 'creds.json'
# ID Google Sheets документа (можно взять из его URL)
spreadsheet_id = '1PwgkG6nqIQqj7KiXRv19Hcy0igg9EfS6kkG2gfVDgzI'

# Авторизуемся и получаем service — экземпляр доступа к API
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)

def sheetWriteAnswer(number, answer):
    # Пример записи в файл
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

def sheetWriteQuestion (number, question):
    # Пример записи в файл
    number
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
