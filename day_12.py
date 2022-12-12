from pathlib import Path
from typing import Callable, List, Tuple

import numpy as np

from constants import INPUTS_DIR, UTF_8

StepCheck = Callable[[int, int], bool]
EndCheck = Callable[[Tuple[int, int]], bool]

INPUT_PATH = Path(INPUTS_DIR) / "day-12.txt"
# INPUT_PATH = Path(INPUTS_DIR) / "example.txt"


START = "S"
END = "E"


def letter_to_num(c: str) -> int:
    return ord(c) - ord("a")


LOWEST = letter_to_num("a")


def parse(lines: List[str]) -> Tuple[np.ndarray, Tuple[int, int], Tuple[int, int]]:
    n_rows = len(lines)
    n_cols = len(lines[0])
    grid = np.empty((n_rows, n_cols), dtype=int)
    for i in range(n_rows):
        for j in range(n_cols):
            c = lines[i][j]
            if c == START:
                start = (i, j)
                val = letter_to_num("a")
            elif c == END:
                end = (i, j)
                val = letter_to_num("z")
            else:
                val = letter_to_num(c)
            grid[i, j] = val
    return grid, start, end


def add_tups(t1: Tuple[int, int], t2: Tuple[int, int]) -> Tuple[int, int]:
    return t1[0] + t2[0], t1[1] + t2[1]


def is_in_bounds(pos: Tuple[int, int], shape: Tuple[int, int]) -> bool:
    return (0 <= pos[0] < shape[0]) and (0 <= pos[1] < shape[1])


def main(
        grid: np.ndarray,
        start: Tuple[int, int],
        *,
        step_check: StepCheck,
        end_check: EndCheck,
) -> int:
    if end_check(start):
        return 0
    visited = np.zeros_like(grid, dtype=bool)
    q = [start]
    steps = 0
    while True:
        new_q = []
        steps += 1
        for cur_pos in q:
            this_level = grid[cur_pos]
            for shift in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                next_pos = add_tups(cur_pos, shift)
                if not is_in_bounds(next_pos, grid.shape) or visited[next_pos]:
                    continue
                next_level = grid[next_pos]
                if not step_check(this_level, next_level):
                    continue
                if end_check(next_pos):
                    return steps
                visited[next_pos] = True
                new_q.append(next_pos)
        q = new_q


if __name__ == "__main__":
    with open(INPUT_PATH, "r", encoding=UTF_8) as f:
        lines_ = [line_.strip() for line_ in f.readlines()]
    grid_, start_, end_ = parse(lines_)
    ans = main(
        grid_,
        start_,
        step_check=(lambda cur_lev, next_lev: next_lev - cur_lev <= 1),
        end_check=(lambda pos_: pos_ == end_),
    )
    print("part 1:", ans)
    ans = main(
        grid_,
        end_,
        step_check=(lambda cur_lev, next_lev: cur_lev - next_lev <= 1),
        end_check=(lambda pos_: grid_[pos_] == LOWEST),
    )
    print("part 2:", ans)
