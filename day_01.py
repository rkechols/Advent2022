from pathlib import Path
from typing import List

from constants import INPUTS_DIR, UTF_8


INPUT_PATH = Path(INPUTS_DIR) / "day-01.txt"


def main(lines: List[str], top_k: int = 1) -> int:
    elf_counts = []
    this_elf = 0
    for line in lines:
        line = line.strip()
        if line == "":
            elf_counts.append(this_elf)
            this_elf = 0
        else:
            this_elf += int(line)
    elf_counts.append(this_elf)
    # get top k
    tops = []
    for count in elf_counts:
        tops.append(count)
        tops.sort(reverse=True)
        if len(tops) > top_k:
            del tops[-1]
    return sum(tops)


if __name__ == "__main__":
    with open(INPUT_PATH, "r", encoding=UTF_8) as f:
        lines_ = f.readlines()
    ans = main(lines_, top_k=1)
    print("1 elf:", ans)
    ans = main(lines_, top_k=3)
    print("3 elves:", ans)
