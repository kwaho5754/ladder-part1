import csv
import os

def save_failure(round_number, actual, predicted_top3):
    # 실패한 예측을 failures.csv에 저장 (없으면 생성)
    file_path = "failures.csv"
    predicted_str = ",".join(predicted_top3)

    # 이미 존재하는 경우 중복 저장 방지
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if str(row["회차"]) == str(round_number):
                    print(f"⚠️ 이미 기록된 회차입니다: {round_number}")
                    return

    with open(file_path, "a", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        if f.tell() == 0:
            writer.writerow(["회차", "실제값", "예측값들"])
        writer.writerow([round_number, actual, predicted_str])
        print(f"❌ 예측 실패 저장됨 → 회차 {round_number} / 실제: {actual} / 예측: {predicted_str}")
