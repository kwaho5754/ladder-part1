import os
from gsheet_handler import get_latest_data
import subprocess

ROUND_FILE = "latest_round.txt"

def get_saved_round():
    if os.path.exists(ROUND_FILE):
        with open(ROUND_FILE, "r", encoding="utf-8") as f:
            return int(f.read().strip())
    return -1

def save_round(round_number):
    with open(ROUND_FILE, "w", encoding="utf-8") as f:
        f.write(str(round_number))

def auto_train_if_new_round():
    df = get_latest_data()
    if df is None or df.empty:
        print("❌ 데이터가 비어 있습니다.")
        return

    latest_round = int(df.iloc[-1]["회차"])
    saved_round = get_saved_round()

    print(f"🔍 최신 회차: {latest_round} / 저장된 회차: {saved_round}")

    if latest_round > saved_round:
        print("✅ 새 회차 감지됨 → 학습 시작")
        subprocess.run(["python", "train_model.py"])
        save_round(latest_round)
    else:
        print("⏭️ 새 회차 없음 → 학습 생략")

if __name__ == "__main__":
    auto_train_if_new_round()
