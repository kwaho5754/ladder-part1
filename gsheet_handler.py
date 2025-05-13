import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json

def get_latest_data():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds_json = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
    creds_dict = json.loads(creds_json)
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)

    client = gspread.authorize(creds)
    spreadsheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1j72Y36aXDYTxsJId92DCnQLouwRgHL2BBOqI9UUDQzE/edit")
    sheet = spreadsheet.worksheet("예측결과")
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
    return df.tail(1000)
