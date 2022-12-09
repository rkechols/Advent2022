from pathlib import Path
from typing import List, Tuple, Set

from constants import INPUTS_DIR, UTF_8

INPUT_PATH = Path(INPUTS_DIR) / "day-09.txt"
# INPUT_PATH = Path(INPUTS_DIR) / "example.txt"


class Knot:
    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y

    def to_tuple(self) -> Tuple[int, int]:
        return self.x, self.y


def step_tail(head: Knot, tail: Knot):
    if head.x == tail.x:
        if head.y > tail.y + 1:
            tail.y += 1
        elif head.y < tail.y - 1:
            tail.y -= 1
    elif head.y == tail.y:
        if head.x > tail.x + 1:
            tail.x += 1
        elif head.x < tail.x - 1:
            tail.x -= 1
    else:  # diagonal
        h_diff = head.x - tail.x
        v_diff = head.y - tail.y
        if abs(h_diff) > 1 or abs(v_diff) > 1:
            h_step = h_diff // abs(h_diff)
            v_step = v_diff // abs(v_diff)
            tail.x += h_step
            tail.y += v_step


def knots_follow(knots: List[Knot], tail_visited: Set[Tuple[int, int]]):
    for i in range(len(knots) - 1):
        step_tail(knots[i], knots[i + 1])
    tail_visited.add(knots[-1].to_tuple())


def main(steps: List[Tuple[str, int]], *, n_knots: int = 2) -> int:
    knots = [Knot() for _ in range(n_knots)]
    tail_visited = {knots[-1].to_tuple()}
    for direction, step_count in steps:
        if direction == "R":
            for _ in range(step_count):
                knots[0].x += 1
                knots_follow(knots, tail_visited)
        elif direction == "L":
            for _ in range(step_count):
                knots[0].x -= 1
                knots_follow(knots, tail_visited)
        elif direction == "U":
            for _ in range(step_count):
                knots[0].y += 1
                knots_follow(knots, tail_visited)
        elif direction == "D":
            for _ in range(step_count):
                knots[0].y -= 1
                knots_follow(knots, tail_visited)
        else:
            ValueError(f"bad direction: {direction}")
    return len(tail_visited)


if __name__ == "__main__":
    with open(INPUT_PATH, "r", encoding=UTF_8) as f:
        steps_ = [line_.strip().split() for line_ in f.readlines()]
    steps_ = [(direction_, int(count)) for direction_, count in steps_]
    ans = main(steps_, n_knots=2)
    print("part 1:", ans)
    ans = main(steps_, n_knots=10)
    print("part 2:", ans)
