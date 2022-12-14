import copy
from pathlib import Path
from typing import Dict, List, Literal, Tuple

from constants import INPUTS_DIR, UTF_8

INPUT_PATH = Path(INPUTS_DIR) / "day-14.txt"
# INPUT_PATH = Path(INPUTS_DIR) / "example.txt"

Loc = Tuple[int, int]


ROCK = "#"
SAND = "o"
AIR = "."

START = (500, 0)


def sign(a: int, b: int) -> Literal[1, -1]:
    if a < b:
        return 1
    elif a > b:
        return -1
    else:  # equal
        raise ValueError("no sign of 0")


class Cave:
    def __init__(self):
        self.data: Dict[Loc, str] = {}

    def loc_is_free(self, loc: Loc) -> bool:
        return self.data.get(loc, AIR) not in (ROCK, SAND)

    def __getitem__(self, key: Loc) -> str:
        return self.data[key]

    def __setitem__(self, key: Loc, value: str):
        self.data[key] = value

    def draw(self):
        min_x = min(x for x, _ in self.data.keys())
        max_x = max(x for x, _ in self.data.keys())
        min_y = min(y for _, y in self.data.keys())
        max_y = max(y for _, y in self.data.keys())
        n_rows = 1 + max_y - min_y
        n_cols = 1 + max_x - min_x
        canvas = [
            [AIR for _ in range(n_cols)]
            for _ in range(n_rows)
        ]
        for (x, y), val in self.data.items():
            canvas[y - min_y][x - min_x] = val
        print("\n".join("".join(row) for row in canvas))

    def lowest_rock(self) -> int:
        return max(
            y
            for (_, y), val in self.data.items()
            if val == ROCK
        )


class Sand:
    def __init__(self, loc: Loc):
        self.x, self.y = loc

    def fall(self, cave: Cave, floor: int = None) -> bool:
        next_y = self.y + 1
        if next_y == floor:
            return False
        if cave.loc_is_free(next_loc := (self.x, next_y)) \
                or cave.loc_is_free(next_loc := (self.x - 1, next_y)) \
                or cave.loc_is_free(next_loc := (self.x + 1, next_y)):
            self.x, self.y = next_loc
            return True
        # can't go anywhere
        return False

    @property
    def loc(self) -> Loc:
        return self.x, self.y


def parse(lines: List[str]) -> Cave:
    cave = Cave()
    for line in lines:
        prev = None
        for point_str in line.split("->"):
            cur = tuple(map(int, point_str.strip().split(",")))
            if prev is not None:
                if prev[0] == cur[0]:
                    pair = prev[1], cur[1]
                    for y in range(*pair, sign(*pair)):
                        cave[(prev[0], y)] = ROCK
                elif prev[1] == cur[1]:
                    pair = prev[0], cur[0]
                    for x in range(*pair, sign(*pair)):
                        cave[(x, prev[1])] = ROCK
                else:
                    raise ValueError(f"cannot draw line from {prev} to {cur}")
            prev = cur
        cave[prev] = ROCK
    return cave


def main(cave: Cave, *, floor_terminates) -> int:
    cave = copy.deepcopy(cave)
    count = 0
    lowest = cave.lowest_rock()
    floor = lowest + 2
    path = [START]
    while cave.loc_is_free(START):
        cur = Sand(path[-1])
        while cur.fall(cave, floor):
            path.append(cur.loc)
            if floor_terminates and cur.y > lowest:
                # it went below lowest rock; next move would hit the floor
                return count
        path.pop()  # next sand starts where this one just came from
        cave[cur.loc] = SAND
        count += 1
    return count


if __name__ == "__main__":
    with open(INPUT_PATH, "r", encoding=UTF_8) as f:
        lines_ = [line_.strip() for line_ in f.readlines()]
    cave_ = parse(lines_)
    cave_.draw()
    ans = main(cave_, floor_terminates=True)
    print("part 1:", ans)
    ans = main(cave_, floor_terminates=False)
    print("part 2:", ans)
