import os
import json
import pandas as pd
import gspread
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials

# .env.local에서 환경 변수 로드
load_dotenv(dotenv_path=".env.local")

# 서비스 계정 JSON 환경 변수 로드
creds_json = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
if creds_json is None:
    print("❌ 환경 변수 GOOGLE_SERVICE_ACCOUNT_JSON이 설정되지 않았습니다.")
    exit(1)

# JSON 문자열을 dict로 변환 (이중 파싱 방어 포함)
try:
    creds_dict = json.loads(creds_json)
    if isinstance(creds_dict, str):
        creds_dict = json.loads(creds_dict)
except Exception as e:
    print("❌ JSON 파싱 중 오류:", e)
    exit(1)

# 인증 및 시트 접근
scope = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/drive.readonly",
]

try:
    creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
    client = gspread.authorize(creds)
except Exception as e:
    print("❌ Google 인증 중 오류 발생:", e)
    exit(1)

# 시트 이름
SPREADSHEET_NAME = "실시간사다리"

def get_latest_data():
    try:
        sheet = client.open(SPREADSHEET_NAME).worksheet("예측결과")
        data = sheet.get_all_records()

        if not data or len(data) == 0:
            print("⚠️ 시트는 열렸지만 데이터가 없습니다.")
            return None

        df = pd.DataFrame(data)

        # ✅ 최근 1000줄 기준으로 잘라서 반환
        if len(df) > 1000:
            df = df.tail(1000).reset_index(drop=True)

        return df

    except Exception as e:
        print("❌ 시트 데이터 불러오기 중 오류 발생:", e)
        return None
