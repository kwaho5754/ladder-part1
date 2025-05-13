import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import os

def get_latest_data():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    
    creds_json = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
    if not creds_json:
        raise RuntimeError("환경변수 GOOGLE_SERVICE_ACCOUNT_JSON이 설정되지 않았습니다.")
    
    # 🔧 private_key 줄바꿈 복원 처리
    creds_dict = json.loads(creds_json)
    creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")

    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)

    # ✅ 시트 주소 직접 지정
    spreadsheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1j72Y36aXDYTxsJId92DCnQLouwRgHL2BBOqI9UUDQzE/edit")
    worksheet = spreadsheet.worksheet("예측결과")

    data = worksheet.get_all_records()
    df = pd.DataFrame(data)

    return df.tail(1000)
