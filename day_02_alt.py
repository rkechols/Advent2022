from pathlib import Path
from typing import List, Tuple

from constants import INPUTS_DIR, UTF_8

INPUT_PATH = Path(INPUTS_DIR) / "day-02.txt"
# INPUT_PATH = Path(INPUTS_DIR) / "example.txt"

ORDER_THEM = "ABC"
ORDER_ME = "XYZ"


def main1(lines: List[Tuple[str, str]]) -> int:
    total = 0
    for them, me in lines:
        them_index = ORDER_THEM.index(them)
        me_index = ORDER_ME.index(me)
        total += me_index + 1  # for item
        total += ((1 + me_index - them_index) % 3) * 3  # for win
    return total


def main2(lines: List[Tuple[str, str]]) -> int:
    total = 0
    for them, me in lines:
        them_index = ORDER_THEM.index(them)
        me_index = ORDER_ME.index(me)
        total += 1 + ((them_index + me_index - 1) % 3)  # for item
        total += me_index * 3  # for win
    return total


if __name__ == "__main__":
    with open(INPUT_PATH, "r", encoding=UTF_8) as f:
        lines_ = f.readlines()
    lines_ = [line_.strip().split() for line_ in lines_]
    ans = main1(lines_)
    print("part 1:", ans)
    ans = main2(lines_)
    print("part 2:", ans)
