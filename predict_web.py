from flask import Flask
import os
import joblib
from gsheet_handler import get_latest_data
from pattern_analyzer import analyze_patterns
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)

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
        return predicted_combo  # 예외 발생 시 fallback

@app.route("/predict")
def predict():
    data = get_latest_data()
    top_combos = analyze_patterns(data)

    predict_round = data[-1]["회차"] + 1
    predictions = []

    for i, combo in enumerate(top_combos[:3], start=1):
        predicted = predict_with_model(combo)
        formatted = f"{i}. {predicted[0]} / {predicted[1]} / {predicted[2]}"
        predictions.append(formatted)

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
