from pathlib import Path
from typing import List

import numpy as np

from constants import INPUTS_DIR, UTF_8

INPUT_PATH = Path(INPUTS_DIR) / "day-08.txt"
# INPUT_PATH = Path(INPUTS_DIR) / "example.txt"


def main1(grid: List[List[int]]) -> int:
    n_rows = len(grid)
    n_cols = len(grid[0])
    visible = np.zeros((n_rows, n_cols), dtype=bool)
    visible[0, :] = True
    visible[-1, :] = True
    visible[:, 0] = True
    visible[:, -1] = True
    for row in range(n_rows):
        # from left
        tallest = grid[row][0]
        for col in range(1, n_cols):
            if grid[row][col] > tallest:
                tallest = grid[row][col]
                visible[row, col] = True
        # from right
        tallest = grid[row][-1]
        for col in range(n_cols - 2, -1, -1):
            if grid[row][col] > tallest:
                tallest = grid[row][col]
                visible[row, col] = True
    for col in range(n_cols):
        # from up
        tallest = grid[0][col]
        for row in range(1, n_rows):
            if grid[row][col] > tallest:
                tallest = grid[row][col]
                visible[row, col] = True
        # from down
        tallest = grid[-1][col]
        for row in range(n_rows - 2, -1, -1):
            if grid[row][col] > tallest:
                tallest = grid[row][col]
                visible[row, col] = True
    return visible.sum()


def score(forest: List[List[int]], row: int, col: int) -> int:
    n_rows = len(forest)
    n_cols = len(forest[0])
    this_height = forest[row][col]
    # up
    for i in range(row - 1, -1, -1):
        if forest[i][col] >= this_height:
            up = row - i
            break
    else:
        up = row
    # down
    for i in range(row + 1, n_rows):
        if forest[i][col] >= this_height:
            down = i - row
            break
    else:
        down = n_rows - row - 1
    # left
    for i in range(col - 1, -1, -1):
        if forest[row][i] >= this_height:
            left = col - i
            break
    else:
        left = col
    # right
    for i in range(col + 1, n_cols):
        if forest[row][i] >= this_height:
            right = i - col
            break
    else:
        right = n_cols - col - 1
    return up * down * left * right


def main2(forest: List[List[int]]) -> int:
    highest = 0
    for i in range(1, len(forest) - 1):
        for j in range(1, len(forest[0]) - 1):
            highest = max(highest, score(forest, i, j))
    return highest


if __name__ == "__main__":
    with open(INPUT_PATH, "r", encoding=UTF_8) as f:
        forest_ = [list(map(int, line_.strip())) for line_ in f.readlines()]
    ans = main1(forest_)
    print("part 1:", ans)
    ans = main2(forest_)
    print("part 2:", ans)
