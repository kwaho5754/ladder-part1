import os
import csv

def save_failure(predict_round, predicted, actual):
    os.makedirs("failures", exist_ok=True)
    file_path = "failures/failures.csv"
    file_exists = os.path.isfile(file_path)

    with open(file_path, mode="a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(["회차", "예측_좌우", "예측_줄수", "예측_홀짝", "실제_좌우", "실제_줄수", "실제_홀짝"])
        writer.writerow([
            predict_round,
            predicted[0], predicted[1], predicted[2],
            actual[0], actual[1], actual[2]
        ])
