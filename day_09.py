from pathlib import Path
from typing import List

from constants import INPUTS_DIR, UTF_8

INPUT_PATH = Path(INPUTS_DIR) / "day-09.txt"
# INPUT_PATH = Path(INPUTS_DIR) / "example.txt"


VERTICAL = 0
HORIZONTAL = 1


def step_tail(head, tail):
    if head[HORIZONTAL] == tail[HORIZONTAL]:
        if head[VERTICAL] > tail[VERTICAL] + 1:
            tail[VERTICAL] += 1
        elif head[VERTICAL] < tail[VERTICAL] - 1:
            tail[VERTICAL] -= 1
    elif head[VERTICAL] == tail[VERTICAL]:
        if head[HORIZONTAL] > tail[HORIZONTAL] + 1:
            tail[HORIZONTAL] += 1
        elif head[HORIZONTAL] < tail[HORIZONTAL] - 1:
            tail[HORIZONTAL] -= 1
    else:  # diagonal
        h_diff = head[HORIZONTAL] - tail[HORIZONTAL]
        v_diff = head[VERTICAL] - tail[VERTICAL]
        if abs(h_diff) > 1 or abs(v_diff) > 1:
            h_step = h_diff // abs(h_diff)
            v_step = v_diff // abs(v_diff)
            tail[HORIZONTAL] += h_step
            tail[VERTICAL] += v_step


def main(lines: List[str], *, n_knots: int = 2) -> int:
    tail_visited = {(0, 0)}
    knots = [[0, 0] for _ in range(n_knots)]
    for line in lines:
        direction, count = line.split()
        count = int(count)
        if direction == "R":
            for _ in range(count):
                knots[0][HORIZONTAL] += 1
                for i in range(n_knots - 1):
                    step_tail(knots[i], knots[i + 1])
                tail_visited.add(tuple(knots[-1]))
        elif direction == "L":
            for _ in range(count):
                knots[0][HORIZONTAL] -= 1
                for i in range(n_knots - 1):
                    step_tail(knots[i], knots[i + 1])
                tail_visited.add(tuple(knots[-1]))
        elif direction == "U":
            for _ in range(count):
                knots[0][VERTICAL] += 1
                for i in range(n_knots - 1):
                    step_tail(knots[i], knots[i + 1])
                tail_visited.add(tuple(knots[-1]))
        elif direction == "D":
            for _ in range(count):
                knots[0][VERTICAL] -= 1
                for i in range(n_knots - 1):
                    step_tail(knots[i], knots[i + 1])
                tail_visited.add(tuple(knots[-1]))
        else:
            ValueError(f"bad direction: {direction}")
    return len(tail_visited)


if __name__ == "__main__":
    with open(INPUT_PATH, "r", encoding=UTF_8) as f:
        lines_ = [line_.strip() for line_ in f.readlines()]
    ans = main(lines_, n_knots=2)
    print("part 1:", ans)
    ans = main(lines_, n_knots=10)
    print("part 2:", ans)
