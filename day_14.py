import copy
from pathlib import Path
from typing import List, Dict, Tuple

from constants import INPUTS_DIR, UTF_8

INPUT_PATH = Path(INPUTS_DIR) / "day-14.txt"
# INPUT_PATH = Path(INPUTS_DIR) / "example.txt"


ROCK = "#"
SAND = "o"
AIR = "."

START = (500, 0)


def sign(a, b) -> int:
    if a < b:
        return 1
    elif a > b:
        return -1
    else:
        raise ValueError("no sign of 0")


def parse(lines: List[str]) -> Dict[Tuple[int, int], str]:
    data = {}
    for line in lines:
        prev = None
        for point_str in line.split("->"):
            cur = tuple(map(int, point_str.strip().split(",")))
            if prev is not None:
                if prev[0] == cur[0]:
                    pair = prev[1], cur[1]
                    for y in range(*pair, sign(*pair)):
                        data[(prev[0], y)] = ROCK
                elif prev[1] == cur[1]:
                    pair = prev[0], cur[0]
                    for x in range(*pair, sign(*pair)):
                        data[(x, prev[1])] = ROCK
                else:
                    raise ValueError(f"cannot draw line from {prev} to {cur}")
            prev = cur
        data[prev] = ROCK
    return data


def draw(data: Dict[Tuple[int, int], str]):
    min_x = min(x for x, _ in data.keys())
    max_x = max(x for x, _ in data.keys())
    min_y = min(y for _, y in data.keys())
    max_y = max(y for _, y in data.keys())
    n_rows = 1 + max_y - min_y
    n_cols = 1 + max_x - min_x
    canvas = [
        [AIR for _ in range(n_cols)]
        for _ in range(n_rows)
    ]
    for (x, y), val in data.items():
        canvas[y - min_y][x - min_x] = val
    for row in canvas:
        print("".join(row))


def main1(data: Dict[Tuple[int, int], str]) -> int:
    data = copy.deepcopy(data)
    count = 0
    lowest = max(y for _, y in data.keys())
    while True:
        cur = START
        at_rest = False
        while cur[1] <= lowest:
            next_y = cur[1] + 1
            if (next_ := (cur[0], next_y)) not in data:
                cur = next_
            elif (next_ := (cur[0] - 1, next_y)) not in data:
                cur = next_
            elif (next_ := (cur[0] + 1, next_y)) not in data:
                cur = next_
            else:  # stops here
                data[cur] = SAND
                at_rest = True
                break
        if at_rest:
            count += 1
        else:
            break
    return count


def main2(data: Dict[Tuple[int, int], str]) -> int:
    data = copy.deepcopy(data)
    count = 0
    floor = max(y for _, y in data.keys()) + 2
    while data.get(START, AIR) not in (ROCK, SAND):
        cur = START
        at_rest = False
        while not at_rest:
            next_y = cur[1] + 1
            if next_y == floor:
                at_rest = True
            else:
                if (next_ := (cur[0], next_y)) not in data:
                    cur = next_
                elif (next_ := (cur[0] - 1, next_y)) not in data:
                    cur = next_
                elif (next_ := (cur[0] + 1, next_y)) not in data:
                    cur = next_
                else:  # stops here
                    at_rest = True
        data[cur] = SAND
        count += 1
    return count


if __name__ == "__main__":
    with open(INPUT_PATH, "r", encoding=UTF_8) as f:
        lines_ = [line_.strip() for line_ in f.readlines()]
    data_ = parse(lines_)
    # draw(data_)
    ans = main1(data_)
    print("part 1:", ans)
    ans = main2(data_)
    print("part 2:", ans)
