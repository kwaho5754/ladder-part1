import pandas as pd
import os
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

def train_failure_model():
    path = "failures/failures.csv"
    if not os.path.exists(path):
        print("오답 데이터가 없습니다.")
        return

    df = pd.read_csv(path)

    X = df[["예측_좌우", "예측_줄수", "예측_홀짝"]].astype(str)
    y = df[["실제_좌우", "실제_줄수", "실제_홀짝"]].astype(str)

    # 각각의 라벨을 숫자로 인코딩
    encoders = [LabelEncoder() for _ in range(3)]
    X_enc = pd.DataFrame({col: enc.fit_transform(X[col]) for enc, col in zip(encoders, X.columns)})
    y_enc = pd.DataFrame({col: enc.fit_transform(y[col]) for enc, col in zip(encoders, y.columns)})

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_enc, y_enc)

    os.makedirs("model", exist_ok=True)
    joblib.dump((model, encoders), "model/model.pkl")
    print("✅ 모델 학습 완료 및 저장: model/model.pkl")

if __name__ == "__main__":
    train_failure_model()
