import bisect
from pathlib import Path
from typing import List

from constants import INPUTS_DIR, UTF_8

INPUT_PATH = Path(INPUTS_DIR) / "day-01.txt"


def parse(input_raw: str) -> List[List[int]]:
    blocks = input_raw.strip().split("\n\n")
    to_return = [
        list(map(int, block.split("\n")))
        for block in blocks
    ]
    return to_return


def main(blocks: List[List[int]], top_k: int = 1) -> int:
    elf_counts = [
        sum(block)
        for block in blocks
    ]
    # get top k
    tops = []
    for count in elf_counts:
        bisect.insort(tops, count, key=lambda x: -x)  # insertion that maintains descending order
        if len(tops) > top_k:
            del tops[-1]
    return sum(tops)


if __name__ == "__main__":
    with open(INPUT_PATH, "r", encoding=UTF_8) as f:
        input_raw_ = f.read()
    blocks_ = parse(input_raw_)
    ans = main(blocks_, top_k=1)
    print("1 elf:", ans)
    ans = main(blocks_, top_k=3)
    print("3 elves:", ans)
