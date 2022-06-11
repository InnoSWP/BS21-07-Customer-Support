
import string
from pprint import pprint

import apiclient
import httplib2
from oauth2client.service_account import ServiceAccountCredentials

first = ['First question', 'First answer']
second = ['Second question', 'Second answer']
general = []
general += first, second

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

# Пример чтения файла
values = service.spreadsheets().values().get(
    spreadsheetId=spreadsheet_id,
    range='A1:B3',
    majorDimension='COLUMNS'
).execute()
pprint(values)

# Пример записи в файл
values = service.spreadsheets().values().batchUpdate(
    spreadsheetId=spreadsheet_id,
    body={
        "valueInputOption": "USER_ENTERED",
        "data": [
            {"range": "A2:B3",
             "majorDimension": "ROWS",
             "values": general},
            {"range": "A4:B5",
             "majorDimension": "COLUMNS",
             "values": [["This is D5", "This is D6"], ["This is E5", "=5+5"]]}
	]
    }

).execute()
