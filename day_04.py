import re
from pathlib import Path
from typing import List

from constants import INPUTS_DIR, UTF_8

INPUT_PATH = Path(INPUTS_DIR) / "day-04.txt"
# INPUT_PATH = Path(INPUTS_DIR) / "example.txt"


RANGE_PAIR_PARSE_RE = re.compile(r"(\d+)-(\d+),(\d+)-(\d+)")


def main1(lines: List[str]):
    count = 0
    for line in lines:
        first_start, first_end, second_start, second_end = \
            map(int, RANGE_PAIR_PARSE_RE.fullmatch(line).groups())
        if first_start <= second_start and first_end >= second_end \
                or second_start <= first_start and second_end >= first_end:
            count += 1
    return count


def main2(lines: List[str]):
    count = 0
    for line in lines:
        first_start, first_end, second_start, second_end = \
            map(int, RANGE_PAIR_PARSE_RE.fullmatch(line).groups())
        if len(
                set(range(first_start, first_end + 1))
                & set(range(second_start, second_end + 1))
        ) > 0:
            count += 1
    return count


if __name__ == "__main__":
    with open(INPUT_PATH, "r", encoding=UTF_8) as f:
        lines_ = [line_.strip() for line_ in f.readlines()]
    ans = main1(lines_)
    print("total overlap:", ans)
    ans = main2(lines_)
    print("partial overlap:", ans)
