import re
from pathlib import Path
from typing import List, Tuple

import z3

from constants import INPUTS_DIR, UTF_8

EXAMPLE = False
if EXAMPLE:
    INPUT_PATH = Path(INPUTS_DIR) / "example.txt"
    PART_1_TARGET_Y = 10
    PART_2_DIM_MAX = 20
else:  # for real
    INPUT_PATH = Path(INPUTS_DIR) / "day-15.txt"
    PART_1_TARGET_Y = 2000000
    PART_2_DIM_MAX = 4000000


INTEGER_RE = re.compile(r"-?\d+")


def abs_z3(x):
    return z3.If(x >= 0, x, -x)


def parse(lines: List[str]) -> List[Tuple[int, int, int, int]]:
    return [
        tuple(map(int, INTEGER_RE.findall(line)))
        for line in lines
    ]


def manhattan(p1: Tuple[int, int], p2: Tuple[int, int]) -> int:
    return sum(abs(v1 - v2) for v1, v2 in zip(p1, p2))


def main1(data: List[Tuple[int, int, int, int]]) -> int:
    all_sensors = {(sx, sy) for sx, sy, _, _ in data}
    all_beacons = {(bx, by) for _, _, bx, by in data}
    all_known = all_sensors | all_beacons
    x_vals_no_beacon = set()
    for sx, sy, bx, by in data:
        s_to_b = manhattan((sx, sy), (bx, by))
        for x_shift in range(1 + s_to_b - abs(PART_1_TARGET_Y - sy)):
            for shift_direction in (-1, 1):
                x = sx + shift_direction * x_shift
                x_vals_no_beacon.add(x)
    for (x, y) in all_known:
        if y == PART_1_TARGET_Y:
            x_vals_no_beacon.discard(x)
    return len(x_vals_no_beacon)


def main2(data: List[Tuple[int, int, int, int]]) -> int:
    x, y = z3.Ints("x y")
    constraints = [
        x >= 0,
        x <= PART_2_DIM_MAX,
        y >= 0,
        y <= PART_2_DIM_MAX,
    ]
    for sx, sy, bx, by in data:
        distance = manhattan((sx, sy), (bx, by))
        constraint = (abs_z3(sx - x) + abs_z3(sy - y) > distance)
        constraints.append(constraint)
    solver = z3.Solver()
    for c in constraints:
        solver.add(c)
    if solver.check() != z3.sat:
        raise ArithmeticError("cannot find solution")
    result = solver.model()
    x, y = result[x].as_long(), result[y].as_long()
    return (x * 4000000) + y


if __name__ == "__main__":
    with open(INPUT_PATH, "r", encoding=UTF_8) as f:
        lines_ = [line_.strip() for line_ in f.readlines()]
    data_ = parse(lines_)
    ans = main1(data_)
    print("part 1:", ans)
    ans = main2(data_)
    print("part 2:", ans)
