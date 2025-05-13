from collections import Counter

def get_top_predictions(df):
    combo_counter = Counter()

    # 최근 5개씩 블록 만들어 다음 값을 예측하는 방식
    for i in range(len(df) - 4):
        block = df.iloc[i:i+4]
        next_row = df.iloc[i+4]
        combo = (next_row["좌우"], next_row["줄수"], next_row["홀짝"])
        combo_counter[combo] += 1

    # 상위 3개 조합 추출
    top3 = combo_counter.most_common(3)

    try:
        predict_round = int(df["회차"].iloc[-1]) + 1
    except:
        predict_round = "?"

    return top3, predict_round
