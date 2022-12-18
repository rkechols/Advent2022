from collections import deque
from itertools import product as cartesian_product
from pathlib import Path
from typing import Iterable, List, Optional, Set, Tuple

import numpy as np

from constants import INPUTS_DIR, UTF_8

INPUT_PATH = Path(INPUTS_DIR) / "day-18.txt"
# INPUT_PATH = Path(INPUTS_DIR) / "example.txt"


Point = Tuple[int, int, int]
DIM = 3


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


def internal_bfs(start: Point, visited: np.ndarray) -> Optional[Set[Point]]:
    q = deque([start])
    newly_visited = set()
    hit_boundary = False
    while len(q) > 0:
        point = q.popleft()
        visited[point] = True
        newly_visited.add(point)
        for neighbor in get_neighbors(point):
            if neighbor in q:  # don't re-list points we're already planning on visiting
                continue
            if any(val < 0 or val >= visited.shape[i] for i, val in enumerate(neighbor)):
                hit_boundary = True
                continue  # don't go off the grid
            if visited[neighbor]:
                continue  # don't go to points we don't care about
            # new
            q.append(neighbor)
    return newly_visited if not hit_boundary else None


def find_internal_points(arr: np.ndarray) -> Set[Point]:
    visited = arr.copy()
    internal_points: Set[Point] = set()
    for search_start in cartesian_product(*(range(d) for d in visited.shape)):
        if not visited[search_start]:
            if (new_internal_points := internal_bfs(search_start, visited)) is not None:
                internal_points.update(new_internal_points)
    return internal_points


def main2(blob: Set[Point], n_faces_open: int) -> int:
    # put the blob points into an array
    shift = tuple(
        min(point[i] for point in blob)
        for i in range(DIM)
    )
    blob = {
        tuple(p - s for p, s in zip(point, shift))
        for point in blob
    }
    arr_shape = tuple(
        1 + max(point[i] for point in blob)
        for i in range(DIM)
    )
    arr = np.zeros(arr_shape, dtype=bool)
    for point in blob:
        arr[point] = True
    # find where an internal point shares a face with a blob point
    internal_points = find_internal_points(arr)
    n_faces_internal = 0
    for point in internal_points:
        for neighbor in get_neighbors(point):
            if neighbor in blob:
                n_faces_internal += 1
    return n_faces_open - n_faces_internal


if __name__ == "__main__":
    with open(INPUT_PATH, "r", encoding=UTF_8) as f:
        lines_ = [line_.strip() for line_ in f.readlines()]
    blob_ = parse(lines_)
    answer1 = main(blob_)
    print("part 1:", answer1)
    answer2 = main2(blob_, answer1)
    print("part 2:", answer2)
