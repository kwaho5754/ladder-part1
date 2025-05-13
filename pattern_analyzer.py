from collections import Counter

def analyze_block(df, column):
    values = df[column].tolist()
    patterns = []

    for i in range(len(values) - 4):
        block = tuple(values[i:i+4])
        next_val = values[i+4]
        patterns.append((block, next_val))

    counter = Counter()
    for pattern, result in patterns:
        counter[(pattern, result)] += 1

    result_counter = Counter()
    for (_, result), count in counter.items():
        result_counter[result] += count

    return result_counter

def get_top_predictions(df):
    total_counter = Counter()

    for col in ["좌우", "줄수", "홀짝"]:
        result = analyze_block(df, col)
        total_counter.update(result)

    top3 = [item[0] for item in total_counter.most_common(3)]

    try:
        predict_round = int(df["회차"].iloc[-1]) + 1
    except:
        predict_round = "?"

    return top3, predict_round
