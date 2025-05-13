import time
import schedule
import os
from gsheet_handler import get_latest_data
from dotenv import load_dotenv

# 경보 환경변수 로드
load_dotenv(dotenv_path=".env.local")

LATEST_FILE = "latest_round.txt"


def load_latest_saved_round():
    if not os.path.exists(LATEST_FILE):
        return -1
    with open(LATEST_FILE, 'r') as f:
        return int(f.read().strip())


def save_latest_round(round_num):
    with open(LATEST_FILE, 'w') as f:
        f.write(str(round_num))


def run_training():
    try:
        data = get_latest_data()
        if data is None or len(data) == 0:
            print("❌ 시트 데이터 없음. 학습 중단")
            return

        current_round = data[-1]["회차"]
        saved_round = load_latest_saved_round()

        if current_round > saved_round:
            print(f"✅ 새 회차 감지: {current_round} (이전: {saved_round}) → 모델 재학습 시작")
            os.system("python train_model.py")
            save_latest_round(current_round)
        else:
            print(f"☑️ 최신 회차 그대로 ({current_round}) → 재학습 생략")

    except Exception as e:
        print("❌ 자동 학습 중 오류 발생:", e)


# 가장 기본 시간 번개: 5분 간격
schedule.every(5).minutes.do(run_training)

print("⏳ 자동 학습 실행 스케줄러 시작됨 (5분 간격)")
run_training()  # 현재시점 한 번 실행

while True:
    schedule.run_pending()
    time.sleep(1)
