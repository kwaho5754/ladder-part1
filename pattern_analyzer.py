from collections import Counter

# 좌우, 홀짝 대칭 정의
def get_mirrored_value(field, value):
    mirrors = {
        '좌우': {'LEFT': 'RIGHT', 'RIGHT': 'LEFT'},
        '홀짝': {'ODD': 'EVEN', 'EVEN': 'ODD'}
    }
    return mirrors[field].get(value, value)

# ✔ DataFrame을 iterrows로 안전하게 순회하도록 수정
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
    patterns = []
    for size in range(min_block, max_block + 1):
        for i in range(size - 1, len(df)):
            normal = extract_pattern_block(df, i, size, reverse=False)
            reverse = extract_pattern_block(df, i - size + 1, size, reverse=True) if i - size + 1 >= 0 else None
            if normal: patterns.append(normal)
            if reverse: patterns.append(reverse)
    return patterns

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
            next_combos.append(get_mirrored_combo(combo))  # 대칭 포함

    counter = Counter(next_combos)
    top_3 = counter.most_common(3)
    return [item[0] for item in top_3]
