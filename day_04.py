import re
from pathlib import Path
from typing import List, Tuple, cast

from constants import INPUTS_DIR, UTF_8

INPUT_PATH = Path(INPUTS_DIR) / "day-04.txt"
# INPUT_PATH = Path(INPUTS_DIR) / "example.txt"


RANGE_PAIR_PARSE_RE = re.compile(r"(\d+)-(\d+),(\d+)-(\d+)")


def parse(lines: List[str]) -> List[Tuple[int, int, int, int]]:
    return [
        cast(
            Tuple[int, int, int, int],
            tuple(map(int, RANGE_PAIR_PARSE_RE.fullmatch(line).groups()))
        )
        for line in lines
    ]


def main1(lines: List[Tuple[int, int, int, int]]):
    count = 0
    for first_start, first_end, second_start, second_end in lines:
        if first_start <= second_start and first_end >= second_end \
                or second_start <= first_start and second_end >= first_end:
            count += 1
    return count


def main2(lines: List[Tuple[int, int, int, int]]):
    count = 0
    for first_start, first_end, second_start, second_end in lines:
        if len(
                set(range(first_start, first_end + 1))
                & set(range(second_start, second_end + 1))
        ) > 0:
            count += 1
    return count


if __name__ == "__main__":
    with open(INPUT_PATH, "r", encoding=UTF_8) as f:
        lines_ = [line_.strip() for line_ in f.readlines()]
    lines_ = parse(lines_)
    ans = main1(lines_)
    print("total overlap:", ans)
    ans = main2(lines_)
    print("partial overlap:", ans)
