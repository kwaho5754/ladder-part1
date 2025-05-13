from flask import Flask
import os
import joblib
import json
from gsheet_handler import get_latest_data
from pattern_analyzer import analyze_patterns
from sklearn.preprocessing import LabelEncoder
from save_failure import save_failure

app = Flask(__name__)

CACHE_FILE = "prediction_cache.json"


def predict_with_model(predicted_combo):
    model_path = "model/model.pkl"
    if not os.path.exists(model_path):
        return predicted_combo  # 모델 없으면 원래 예측값 사용

    model, encoders = joblib.load(model_path)
    input_data = [[predicted_combo[0], str(predicted_combo[1]), predicted_combo[2]]]

    try:
        input_enc = [enc.transform([v])[0] for enc, v in zip(encoders, input_data[0])]
        output_enc = model.predict([input_enc])[0]
        output = [enc.inverse_transform([v])[0] for enc, v in zip(encoders, output_enc)]
        return tuple(output)
    except Exception:
        return predicted_combo


def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_cache(round_number, predictions):
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump({"round": round_number, "predictions": predictions}, f, ensure_ascii=False)


@app.route("/predict")
def predict():
    data = get_latest_data()
    predict_round = data[-1]["회차"] + 1
    last_result = data[-1]["결과"]

    cache = load_cache()
    if cache.get("round") == predict_round:
        cached_predictions = cache["predictions"]
        html = f"""
        <h1>타다리 예측 결과 (캐시)</h1>
        <p><strong>예측 회차:</strong> {predict_round}회차</p>
        <ol>
            <li>{cached_predictions[0]}</li>
            <li>{cached_predictions[1]}</li>
            <li>{cached_predictions[2]}</li>
        </ol>
        """
        return html

    top_combos = analyze_patterns(data)
    predictions = []
    predicted_top3 = []

    for i, combo in enumerate(top_combos[:3], start=1):
        predicted = predict_with_model(combo)
        formatted = f"{i}. {predicted[0]} / {predicted[1]} / {predicted[2]}"
        predictions.append(formatted)
        predicted_top3.append(predicted[0])

    # 오답 기록
    if last_result not in predicted_top3:
        save_failure(data[-1]["회차"], last_result, predicted_top3)

    save_cache(predict_round, predictions)

    html = f"""
    <h1>타다리 예측 결과</h1>
    <p><strong>예측 회차:</strong> {predict_round}회차</p>
    <ol>
        <li>{predictions[0]}</li>
        <li>{predictions[1]}</li>
        <li>{predictions[2]}</li>
    </ol>
    """
    return html


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
