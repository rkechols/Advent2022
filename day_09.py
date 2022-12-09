from pathlib import Path
from typing import List, Tuple

from constants import INPUTS_DIR, UTF_8

INPUT_PATH = Path(INPUTS_DIR) / "day-09.txt"
# INPUT_PATH = Path(INPUTS_DIR) / "example.txt"


class Knot:

    DIRECTIONS = {
        "R": (1, 0),
        "L": (-1, 0),
        "U": (0, 1),
        "D": (0, -1),
    }

    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y

    def shift(self, dir_tuple: Tuple[int, int]):
        self.x += dir_tuple[0]
        self.y += dir_tuple[1]

    def follow(self, head: 'Knot'):
        if head.x == self.x:
            if head.y > self.y + 1:
                self.y += 1
            elif head.y < self.y - 1:
                self.y -= 1
        elif head.y == self.y:
            if head.x > self.x + 1:
                self.x += 1
            elif head.x < self.x - 1:
                self.x -= 1
        else:  # diagonal
            x_diff = head.x - self.x
            y_diff = head.y - self.y
            if abs(x_diff) > 1 or abs(y_diff) > 1:
                x_step = x_diff // abs(x_diff)
                y_step = y_diff // abs(y_diff)
                self.shift((x_step, y_step))

    def to_tuple(self) -> Tuple[int, int]:
        return self.x, self.y


def main(steps: List[Tuple[str, int]], *, n_knots: int = 2) -> int:
    knots = [Knot() for _ in range(n_knots)]
    tail_visited = {knots[-1].to_tuple()}
    for direction, step_count in steps:
        head_shift = Knot.DIRECTIONS[direction]
        for _ in range(step_count):
            knots[0].shift(head_shift)
            for i in range(1, n_knots):
                knots[i].follow(knots[i - 1])
            tail_visited.add(knots[-1].to_tuple())
    return len(tail_visited)


if __name__ == "__main__":
    with open(INPUT_PATH, "r", encoding=UTF_8) as f:
        steps_ = [line_.strip().split() for line_ in f.readlines()]
    steps_ = [(direction_, int(count)) for direction_, count in steps_]
    ans = main(steps_, n_knots=2)
    print("part 1:", ans)
    ans = main(steps_, n_knots=10)
    print("part 2:", ans)
