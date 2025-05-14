from collections import Counter

# 블럭 추출
def extract_block(df, index, size, reverse=False):
    if reverse:
        block = df.iloc[index:index + size][::-1]
    else:
        block = df.iloc[index - size + 1:index + 1]
    if len(block) != size:
        return None
    return tuple((row["좌우"], row["줄수"], row["홀짝"]) for _, row in block.iterrows())

# 최신 블럭 추출
def get_latest_blocks(df, min_block=3, max_block=5):
    latest_blocks = []
    for size in range(min_block, max_block + 1):
        if len(df) >= size:
            latest_block = extract_block(df, len(df) - 1, size, reverse=False)
            latest_blocks.append((latest_block, False))  # 정방향
            latest_blocks.append((tuple(reversed(latest_block)), True))  # 역방향
    return latest_blocks

# 과거 블럭 비교 및 다음줄 결과 수집
def analyze_patterns(df, min_block=3, max_block=5):
    results = []
    latest_blocks = get_latest_blocks(df, min_block, max_block)

    for size in range(min_block, max_block + 1):
        for i in range(size - 1, len(df) - 1):  # 마지막 줄은 예측 대상이 될 수 없음
            for latest_block, is_reversed in latest_blocks:
                current_block = extract_block(df, i, size, reverse=is_reversed)
                if current_block == latest_block:
                    next_index = i + 1
                    if next_index < len(df):
                        next_row = df.iloc[next_index]
                        results.append((next_row["좌우"], next_row["줄수"], next_row["홀짝"]))

    # 가장 많이 등장한 조합 Top 3 반환
    counter = Counter(results)
    top_3 = [item[0] for item in counter.most_common(3)]
    return top_3
