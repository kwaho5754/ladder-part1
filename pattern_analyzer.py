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
    top_predictions = {}

    for col in ["좌우", "줄수", "홀짝"]:
        result = analyze_block(df, col)
        top1 = result.most_common(1)[0][0] if result else "?"
        top_predictions[col] = top1

    try:
        predict_round = int(df["회차"].iloc[-1]) + 1
    except:
        predict_round = "?"

    return top_predictions, predict_round
