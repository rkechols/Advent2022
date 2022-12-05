import copy
import re
from collections import OrderedDict
from pathlib import Path
from typing import List, Tuple, cast

from constants import INPUTS_DIR, UTF_8

INPUT_PATH = Path(INPUTS_DIR) / "day-05.txt"
# INPUT_PATH = Path(INPUTS_DIR) / "example.txt"


def parse(
        start_config: str,
        instructions_block: str,
) -> Tuple[OrderedDict[int, List[str]], List[Tuple[int, int, int]]]:
    # top chunk
    start_config = start_config.split("\n")
    cols = OrderedDict()
    for match in re.finditer(r"\d+", start_config[-1]):
        col = int(match.group())
        loc = match.start()
        this_col = []
        for i in range(len(start_config) - 2, -1, -1):
            line = start_config[i]
            try:  # in case line-final spaces get trimmed
                sym = line[loc]
            except IndexError:
                break
            if sym.isspace():
                break
            this_col.append(sym)
        cols[col] = this_col
    # bottom chunk
    instructions = [
        cast(
            Tuple[int, int, int],
            tuple(map(int, re.fullmatch(r"move (\d+) from (\d+) to (\d+)", instruction).groups()))
        )
        for instruction in instructions_block.strip().split("\n")
    ]
    return cols, instructions


def main1(cols: OrderedDict[int, List[str]], instructions: List[Tuple[int, int, int]]) -> List[str]:
    cols = copy.deepcopy(cols)
    for count, start, end in instructions:
        for i in range(count):
            val = cols[start].pop()
            cols[end].append(val)
    return [col[-1] for col in cols.values()]


def main2(cols: OrderedDict[int, List[str]], instructions: List[Tuple[int, int, int]]) -> List[str]:
    cols = copy.deepcopy(cols)
    for count, start, end in instructions:
        stack = cols[start][-count:]
        del cols[start][-count:]
        cols[end] += stack
    return [col[-1] for col in cols.values()]


if __name__ == "__main__":
    with open(INPUT_PATH, "r", encoding=UTF_8) as f:
        start_config_, instructions_block_ = f.read().split("\n\n")
    cols_, instructions_ = parse(start_config_, instructions_block_)
    ans = main1(cols_, instructions_)
    print("part 1:", "".join(ans))
    ans = main2(cols_, instructions_)
    print("part 2:", "".join(ans))
