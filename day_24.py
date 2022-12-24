from pathlib import Path
from typing import Iterable, List, Optional, Tuple

from constants import INPUTS_DIR, UTF_8

Point = Tuple[int, int]
Field = List[List[Optional[List[str]]]]

INPUT_PATH = Path(INPUTS_DIR) / "day-24.txt"
START = (-1, 0)
END = (25, 119)

# INPUT_PATH = Path(INPUTS_DIR) / "example.txt"
# START = (-1, 0)
# END = (4, 5)

UP = "^"
RIGHT = ">"
DOWN = "v"
LEFT = "<"
EMPTY = "."
WALL = "#"


def _sym_to_slot_val(sym: str) -> List[str]:
    if sym == EMPTY:
        return []  # no blizzards
    elif sym in (UP, RIGHT, DOWN, LEFT):
        return [sym]
    else:
        raise ValueError(f"unknown symbol: {sym}")


def parse(lines: List[str]) -> Field:
    # ignores boundaries
    field = [
        [
            _sym_to_slot_val(sym)
            for sym in line[1:-1]
        ]
        for line in lines[1:-1]
    ]
    return field


def step_field(field: Field) -> Field:
    n_rows = len(field)
    n_cols = len(field[0])
    # gradually add the new blizzard locations to this
    new_field = [
        [
            []
            for _ in range(n_cols)
        ]
        for _ in range(n_rows)
    ]
    for i, row in enumerate(field):
        for j, loc_blizzards in enumerate(row):
            for blizz in loc_blizzards:
                # where will it go next?
                if blizz == UP:
                    new_row = i - 1
                    if new_row < 0:
                        new_row = n_rows - 1
                    new_col = j
                elif blizz == RIGHT:
                    new_row = i
                    new_col = j + 1
                    if new_col >= n_cols:
                        new_col = 0
                elif blizz == DOWN:
                    new_row = i + 1
                    if new_row >= n_rows:
                        new_row = 0
                    new_col = j
                elif blizz == LEFT:
                    new_row = i
                    new_col = j - 1
                    if new_col < 0:
                        new_col = n_cols - 1
                else:
                    raise ValueError(f"unknown blizz value: {blizz}")
                new_field[new_row][new_col].append(blizz)
    return new_field


class FieldSystem:
    def __init__(self, start_field: Field):
        n_rows = len(start_field)
        n_cols = len(start_field[0])
        self.n_steps_cycle = n_rows * n_cols
        self.order = [start_field]

    def __getitem__(self, index: int) -> Field:
        if index < 0:
            raise IndexError(f"cannot get negative index: {index}")
        index %= self.n_steps_cycle  # the system is cyclical
        n_steps_missing = 1 + index - len(self.order)
        if n_steps_missing > 0:
            # iteratively calculate more steps
            cur = self.order[-1]
            for _ in range(n_steps_missing):
                cur = step_field(cur)
                self.order.append(cur)
        return self.order[index]

    def __len__(self) -> int:
        return self.n_steps_cycle


def get_neighbors(point: Point) -> Iterable[Point]:
    yield point  # it's okay to stay still
    for shift in ((0, -1), (0, 1), (-1, 0), (1, 0)):
        yield point[0] + shift[0], point[1] + shift[1]


def is_open(point: Point, field: Field) -> bool:
    n_rows = len(field)
    n_cols = len(field[0])
    if not (0 <= point[0] < n_rows and 0 <= point[1] < n_cols):
        return False  # out of bounds
    slot_val = field[point[0]][point[1]]
    return len(slot_val) == 0  # no blizzards


def main(fields: FieldSystem, skip_steps: int = 0, start: Point = START, end: Point = END) -> int:
    n = len(fields)
    step_num = skip_steps
    locs = {start}
    # cyclical history; if we make it past a full cycle,
    # don't bother re-searching the same paths through the same blizzard patterns
    historical_locs = [
        set()
        for _ in range(n)
    ]
    historical_locs[step_num].add(start)
    # start the BFS
    while True:
        step_num += 1
        # what the new field looks like
        field = fields[step_num]
        historical = historical_locs[step_num % n]
        # figure out all the places we could be by the end of this step
        new_locs = set()
        for loc in locs:  # each place we could be at the start of the step
            for neighbor in get_neighbors(loc):
                if neighbor == end:  # short circuit the search
                    return step_num
                if (neighbor == start or is_open(neighbor, field)) and neighbor not in historical:
                    new_locs.add(neighbor)  # valid option
        if len(new_locs) == 0:  # didn't find anywhere we could go
            raise RuntimeError("ALGORITHM ERROR: dead end")
        historical.update(new_locs)
        locs = new_locs  # prep next step


if __name__ == "__main__":
    with open(INPUT_PATH, "r", encoding=UTF_8) as f:
        lines_ = [line_.strip() for line_ in f.readlines()]
    field_ = parse(lines_)
    fields_ = FieldSystem(field_)
    answer1 = main(fields_)
    print("part 1:", answer1)
    answer2_half = main(fields_, skip_steps=answer1, start=END, end=START)
    print("part 1.5:", answer2_half)
    answer2 = main(fields_, skip_steps=answer2_half)
    print("part 2:", answer2)
