from collections import Counter

# 좌우, 홀짝 대칭 정의
def get_mirrored_value(field, value):
    mirrors = {
        '좌우': {'LEFT': 'RIGHT', 'RIGHT': 'LEFT'},
        '홀짝': {'ODD': 'EVEN', 'EVEN': 'ODD'}
    }
    return mirrors[field].get(value, value)

def extract_pattern_block(data, index, size, reverse=False):
    block = data[index - size + 1:index + 1] if not reverse else data[index:index + size][::-1]
    if len(block) < size:
        return None
    return tuple(
        (
            row['좌우'],
            row['줄수'],
            row['홀짝']
        )
        for row in block
    )

def generate_all_patterns(data, min_block=3, max_block=5):
    patterns = []
    for size in range(min_block, max_block + 1):
        for i in range(size - 1, len(data)):
            normal = extract_pattern_block(data, i, size, reverse=False)
            reverse = extract_pattern_block(data, i - size + 1, size, reverse=True) if i - size + 1 >= 0 else None
            if normal: patterns.append(normal)
            if reverse: patterns.append(reverse)
    return patterns

def get_next_combo(block):
    if not block: return None
    last = block[-1]
    return (last[0], last[1], last[2])

def get_mirrored_combo(combo):
    return (
        get_mirrored_value('좌우', combo[0]),
        combo[1],
        get_mirrored_value('홀짝', combo[2])
    )

def analyze_patterns(data):
    patterns = generate_all_patterns(data)
    next_combos = []

    for i in range(len(patterns)):
        combo = get_next_combo(patterns[i])
        if combo:
            next_combos.append(combo)
            next_combos.append(get_mirrored_combo(combo))  # 대칭 조합도 포함

    counter = Counter(next_combos)
    top_3 = counter.most_common(3)
    return [item[0] for item in top_3]
