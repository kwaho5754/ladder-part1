from flask import Flask, render_template_string
from pattern_analyzer import get_top_predictions
from gsheet_handler import get_latest_data
import os

app = Flask(__name__)

@app.route('/predict')
def predict():
    df = get_latest_data()
    top3, round_num = get_top_predictions(df)

    return render_template_string("""
        <h2>사다리 예측 결과</h2>
        <p><strong>예측 회차:</strong> {{ round_num }}회차</p>
        <ol>
        {% for val in top3 %}
            <li>{{ val }}</li>
        {% endfor %}
        </ol>
    """, top3=top3, round_num=round_num)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))  # Railway가 넘겨주는 포트 자동 인식
    app.run(host="0.0.0.0", port=port)
