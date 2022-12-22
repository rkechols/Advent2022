from collections import deque
from pathlib import Path
from typing import Iterable, List, Set, Tuple

import numpy as np

from constants import INPUTS_DIR, UTF_8

INPUT_PATH = Path(INPUTS_DIR) / "day-18.txt"
# INPUT_PATH = Path(INPUTS_DIR) / "example.txt"


Point = Tuple[int, int, int]
DIM = 3
ORIGIN = (0, 0, 0)


def parse(lines: List[str]) -> Set[Point]:
    to_return = {
        tuple(map(int, line.split(",")))
        for line in lines
    }
    return to_return


def get_neighbors(point: Point) -> Iterable[Point]:
    for index in range(DIM):
        for shift in (-1, 1):
            yield tuple(
                val + shift if i == index else val
                for i, val in enumerate(point)
            )
    return


def main(blob: Set[Point]) -> int:
    open_faces = len(blob) * DIM * 2
    for point in blob:
        for neighbor in get_neighbors(point):
            if neighbor in blob:
                # remove one now, and remove one later when the paired point is checked
                open_faces -= 1
    return open_faces


def main2(blob: Set[Point], n_faces_open: int) -> int:
    # put the blob points into an array
    shift = tuple(
        min(point[i] for point in blob)
        for i in range(DIM)
    )
    blob = {
        # add 1 in each dim for padding
        tuple(1 + p - s for p, s in zip(point, shift))
        for point in blob
    }
    arr_shape = tuple(
        # add padding on the top end too
        2 + max(point[i] for point in blob)
        for i in range(DIM)
    )
    visited = np.zeros(arr_shape, dtype=bool)
    for point in blob:
        visited[point] = True
    # find where an external point shares a face with a blob point
    n_faces_external = 0
    q = deque([ORIGIN])
    while len(q) > 0:
        point = q.popleft()
        visited[point] = True
        for neighbor in get_neighbors(point):
            if neighbor in blob:
                n_faces_external += 1
                continue  # won't be visitable
            if any(val < 0 or val >= visited.shape[i] for i, val in enumerate(neighbor)):
                continue  # don't go off the grid
            if visited[neighbor]:
                continue  # don't go to points already checked
            if neighbor in q:  # don't re-list points we're already planning on visiting
                continue
            # new
            q.append(neighbor)
    return n_faces_external


if __name__ == "__main__":
    with open(INPUT_PATH, "r", encoding=UTF_8) as f:
        lines_ = [line_.strip() for line_ in f.readlines()]
    blob_ = parse(lines_)
    answer1 = main(blob_)
    print("part 1:", answer1)
    answer2 = main2(blob_, answer1)
    print("part 2:", answer2)
