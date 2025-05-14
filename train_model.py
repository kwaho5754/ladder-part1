import os
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# 시트 데이터 로딩
from gsheet_handler import get_latest_data

def train_model():
    data = get_latest_data()
    if data is None or data.empty:
        print("❌ 학습할 데이터가 없습니다.")
        return

    # ✅ 주요 컬럼 예시 (자신의 구조에 맞게 수정)
    feature_columns = ["홀짝", "좌우", "줄수"]  # 입력값 컬럼
    label_column = "좌우"                      # 정답 컬럼

    # ✅ 실패 데이터 로드 및 결합
    if os.path.exists("failures.csv"):
        failures = pd.read_csv("failures.csv")
        failures = failures.rename(columns={"실제값": label_column})
        for col in feature_columns:
            if col not in failures.columns:
                failures[col] = None  # 예시 목적. 실제 패턴 컬럼은 채워야 정확
        data = pd.concat([data, failures[feature_columns + [label_column]]], ignore_index=True)
        print(f"📌 오답 데이터 포함: {len(failures)}개")

    X = data[feature_columns]
    y = data[label_column]

    # 결측치 제거 또는 전처리
    X = X.fillna(0)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)

    os.makedirs("model", exist_ok=True)
    joblib.dump(model, "model/model1.pkl")
    print("✅ 모델 저장 완료: model/model1.pkl")

if __name__ == "__main__":
    train_model()
