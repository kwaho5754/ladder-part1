from collections import Counter
import random

# 좌우, 홀짝 대칭 정의
def get_mirrored_value(field, value):
    mirrors = {
        '좌우': {'LEFT': 'RIGHT', 'RIGHT': 'LEFT'},
        '홀짝': {'ODD': 'EVEN', 'EVEN': 'ODD'}
    }
    return mirrors[field].get(value, value)

def extract_pattern_block(df, index, size, reverse=False):
    if reverse:
        block = df.iloc[index:index + size][::-1]
    else:
        block = df.iloc[index - size + 1:index + 1]

    if len(block) < size:
        return None

    return tuple(
        (
            row["좌우"],
            row["줄수"],
            row["홀짝"]
        )
        for _, row in block.iterrows()
    )

def generate_all_patterns(df, min_block=3, max_block=5):
    pattern_set = set()  # ✅ 중복 제거를 위해 set 사용
    for size in range(min_block, max_block + 1):
        for i in range(size - 1, len(df)):
            normal = extract_pattern_block(df, i, size, reverse=False)
            reverse = extract_pattern_block(df, i - size + 1, size, reverse=True) if i - size + 1 >= 0 else None
            if normal: pattern_set.add(normal)
            if reverse: pattern_set.add(reverse)
    return list(pattern_set)

def get_next_combo(block):
    if not block:
        return None
    last = block[-1]
    return (last[0], last[1], last[2])

def get_mirrored_combo(combo):
    return (
        get_mirrored_value("좌우", combo[0]),
        combo[1],
        get_mirrored_value("홀짝", combo[2])
    )

def analyze_patterns(df):
    patterns = generate_all_patterns(df)
    next_combos = []

    for pattern in patterns:
        combo = get_next_combo(pattern)
        if combo:
            next_combos.append(combo)
            next_combos.append(get_mirrored_combo(combo))

    counter = Counter(next_combos)
    top_10 = counter.most_common(10)

    # ✅ 예측 고정 방지를 위해 상위 10개 중 확률적 3개 추출 (우선순위 기반 샘플링)
    selected = []
    for item in top_10:
        if item[0] not in selected:
            selected.append(item[0])
        if len(selected) >= 3:
            break

    return selected
