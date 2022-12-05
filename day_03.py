from pathlib import Path
from typing import List

from constants import INPUTS_DIR, UTF_8

INPUT_PATH = Path(INPUTS_DIR) / "day-03.txt"
# INPUT_PATH = Path(INPUTS_DIR) / "example.txt"


def priority(s: str) -> int:
    base_score = 1 + ord(s.lower()) - ord("a")
    if s == s.upper():
        base_score += 26
    return base_score


def main1(lines: List[str]) -> int:
    total = 0
    for line in lines:
        half = len(line) // 2
        left = line[:half]
        right = line[half:]
        overlap: str = next(iter(set(left) & set(right)))
        total += priority(overlap)
    return total


def main2(lines: List[str]) -> int:
    total = 0
    for i in range(0, len(lines), 3):
        group = lines[i:(i + 3)]
        overlap: str = next(iter(set(group[0]) & set(group[1]) & set(group[2])))
        total += priority(overlap)
    return total


if __name__ == "__main__":
    with open(INPUT_PATH, "r", encoding=UTF_8) as f:
        lines_ = [line_.strip() for line_ in f.readlines()]
    ans = main1(lines_)
    print("part 1:", ans)
    ans = main2(lines_)
    print("part 2:", ans)
