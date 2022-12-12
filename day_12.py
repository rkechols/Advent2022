import copy
from pathlib import Path
from typing import Tuple

import numpy as np

from constants import INPUTS_DIR, UTF_8

INPUT_PATH = Path(INPUTS_DIR) / "day-12.txt"
# INPUT_PATH = Path(INPUTS_DIR) / "example.txt"


START = "S"
END = "E"


def letter_to_num(c: str) -> int:
    return ord(c) - ord("a")


def main(grid: np.ndarray, start: Tuple[int, int], end: Tuple[int, int]) -> int:
    visited = np.zeros_like(grid, dtype=bool)
    q = [[start]]
    while True:
        new_q = []
        for path in q:
            cur = path[-1]
            this_level = grid[cur]
            for shift in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                next_pos = (cur[0] + shift[0], cur[1] + shift[1])
                if next_pos[0] < 0 or next_pos[0] >= grid.shape[0] or next_pos[1] < 0 or next_pos[1] >= grid.shape[1]:
                    continue  # out of bounds
                if visited[next_pos]:
                    continue
                next_level = grid[next_pos]
                if next_level - this_level > 1:
                    continue
                if next_pos == end:
                    return len(path)
                new_path = copy.deepcopy(path)
                visited[next_pos] = True
                new_path.append(next_pos)
                new_q.append(new_path)
        q = new_q


def main2(grid: np.ndarray, start: Tuple[int, int]) -> int:
    visited = np.zeros_like(grid, dtype=bool)
    q = [[start]]
    while True:
        new_q = []
        for path in q:
            cur = path[-1]
            this_level = grid[cur]
            for shift in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                next_pos = (cur[0] + shift[0], cur[1] + shift[1])
                if next_pos[0] < 0 or next_pos[0] >= grid.shape[0] or next_pos[1] < 0 or next_pos[1] >= grid.shape[1]:
                    continue  # out of bounds
                if visited[next_pos]:
                    continue
                next_level = grid[next_pos]
                if next_level - this_level < -1:
                    continue
                if next_level == 0:
                    return len(path)
                new_path = copy.deepcopy(path)
                visited[next_pos] = True
                new_path.append(next_pos)
                new_q.append(new_path)
        q = new_q


if __name__ == "__main__":
    with open(INPUT_PATH, "r", encoding=UTF_8) as f:
        lines_ = [line_.strip() for line_ in f.readlines()]

    grid_ = np.empty((len(lines_), len(lines_[0])), dtype=int)
    for i_ in range(len(lines_)):
        for j_ in range(len(lines_[0])):
            c_ = lines_[i_][j_]
            if c_ == START:
                start_ = (i_, j_)
                val_ = letter_to_num("a")
            elif c_ == END:
                end_ = (i_, j_)
                val_ = letter_to_num("z")
            else:
                val_ = letter_to_num(c_)
            grid_[i_, j_] = val_
    ans = main(grid_, start_, end_)
    print("part 1:", ans)
    ans = main2(grid_, end_)
    print("part 2:", ans)
