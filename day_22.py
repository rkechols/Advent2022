import re
from enum import IntEnum
from pathlib import Path
from typing import List, Tuple

from constants import INPUTS_DIR, UTF_8

INPUT_PATH = Path(INPUTS_DIR) / "day-22.txt"
# INPUT_PATH = Path(INPUTS_DIR) / "example.txt"

VOID = " "
WALL = "#"
OPEN = "."

CLOCKWISE = "R"
COUNTER_CLOCKWISE = "L"

CUBE_FACE_SIZE = 50


class Direction(IntEnum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3


def rot_clockwise(d: Direction) -> Direction:
    return Direction((d + 1) % 4)


def rot_counter_clockwise(d: Direction) -> Direction:
    return Direction((d - 1) % 4)


def main(maze: List[str], instructions: List[str]) -> int:
    row = 0
    col = maze[row].index(OPEN)
    d = Direction.RIGHT
    for step in instructions:
        if step == CLOCKWISE:
            d = rot_clockwise(d)
        elif step == COUNTER_CLOCKWISE:
            d = rot_counter_clockwise(d)
        else:  # int
            n_moves = int(step)
            for _ in range(n_moves):
                if d == Direction.RIGHT:
                    if col + 1 >= len(maze[row]) or maze[row][col + 1] == VOID:
                        for first_col in range(col):
                            if maze[row][first_col] != VOID:
                                next_col = first_col
                                break
                        else:
                            raise ValueError("never found the first non-VOID char of the line")
                    else:
                        next_col = col + 1
                    next_row = row
                elif d == Direction.LEFT:
                    if col - 1 < 0 or maze[row][col - 1] == VOID:
                        for last_col in range(len(maze[row]) - 1, col, -1):
                            if maze[row][last_col] != VOID:
                                next_col = last_col
                                break
                        else:
                            raise ValueError("never found the last non-VOID char of the line")
                    else:
                        next_col = col - 1
                    next_row = row
                elif d == Direction.DOWN:
                    if row + 1 >= len(maze) or maze[row + 1][col] == VOID:
                        for first_row in range(row):
                            if maze[first_row][col] != VOID:
                                next_row = first_row
                                break
                        else:
                            raise ValueError("never found the first non-VOID char of the column")
                    else:
                        next_row = row + 1
                    next_col = col
                elif d == Direction.UP:
                    if row - 1 < 0 or maze[row - 1][col] == VOID:
                        for last_row in range(len(maze) - 1, row, -1):
                            if maze[last_row][col] != VOID:
                                next_row = last_row
                                break
                        else:
                            raise ValueError("never found the last non-VOID char of the column")
                    else:
                        next_row = row - 1
                    next_col = col
                else:
                    raise ValueError(f"unexpected direction enum: {d}")
                # check the val of the next col
                if maze[next_row][next_col] == OPEN:
                    row = next_row
                    col = next_col
                elif maze[next_row][next_col] == WALL:
                    break  # no more moves in this direction
                else:
                    raise ValueError(f"expected open or wall, but found {repr(maze[next_row][next_col])}")
    return (1000 * (row + 1)) + (4 * (col + 1)) + d


class CubeMaze:
    def __init__(self, maze: List[str]):
        self.maze = maze
        self._validate()

    def _validate(self):
        for row in range(2 * CUBE_FACE_SIZE):
            for col in range(CUBE_FACE_SIZE):
                if self.maze[row][col] != VOID:
                    raise ValueError("unfolded cube maze did not take expected form")
        for row in range(2 * CUBE_FACE_SIZE, 4 * CUBE_FACE_SIZE):
            for col in range(CUBE_FACE_SIZE):
                if self.maze[row][col] not in (OPEN, WALL):
                    raise ValueError("unfolded cube maze did not take expected form")
        for row in range(3 * CUBE_FACE_SIZE):
            for col in range(CUBE_FACE_SIZE, 2 * CUBE_FACE_SIZE):
                if self.maze[row][col] not in (OPEN, WALL):
                    raise ValueError("unfolded cube maze did not take expected form")
        for row in range(3 * CUBE_FACE_SIZE, 4 * CUBE_FACE_SIZE):
            for col in range(CUBE_FACE_SIZE, 2 * CUBE_FACE_SIZE):
                if self.maze[row][col] != VOID:
                    raise ValueError("unfolded cube maze did not take expected form")
        for row in range(CUBE_FACE_SIZE):
            for col in range(2 * CUBE_FACE_SIZE, 3 * CUBE_FACE_SIZE):
                if self.maze[row][col] not in (OPEN, WALL):
                    raise ValueError("unfolded cube maze did not take expected form")
        for row in range(CUBE_FACE_SIZE, 4 * CUBE_FACE_SIZE):
            for col in range(2 * CUBE_FACE_SIZE, 3 * CUBE_FACE_SIZE):
                if self.maze[row][col] != VOID:
                    raise ValueError("unfolded cube maze did not take expected form")

    def cube_step(self, row: int, col: int, d: Direction) -> Tuple[int, int, Direction]:
        if row == 0 and CUBE_FACE_SIZE <= col < 2 * CUBE_FACE_SIZE and d == Direction.UP:
            return (3 * CUBE_FACE_SIZE) + (col - CUBE_FACE_SIZE), 0, Direction.RIGHT
        elif row == 0 and 2 * CUBE_FACE_SIZE <= col < 3 * CUBE_FACE_SIZE and d == Direction.UP:
            return 4 * CUBE_FACE_SIZE - 1, col - (2 * CUBE_FACE_SIZE), Direction.UP
        elif 0 <= row < CUBE_FACE_SIZE and col == CUBE_FACE_SIZE and d == Direction.LEFT:
            return (3 * CUBE_FACE_SIZE - 1) - row, 0, Direction.RIGHT
        elif 0 <= row < CUBE_FACE_SIZE and col == 3 * CUBE_FACE_SIZE - 1 and d == Direction.RIGHT:
            return (3 * CUBE_FACE_SIZE - 1) - row, 2 * CUBE_FACE_SIZE - 1, Direction.LEFT
        elif row == CUBE_FACE_SIZE - 1 and 2 * CUBE_FACE_SIZE <= col < 3 * CUBE_FACE_SIZE and d == Direction.DOWN:
            return CUBE_FACE_SIZE + (col - 2 * CUBE_FACE_SIZE), 2 * CUBE_FACE_SIZE - 1, Direction.LEFT
        elif CUBE_FACE_SIZE <= row < 2 * CUBE_FACE_SIZE and col == CUBE_FACE_SIZE and d == Direction.LEFT:
            return 2 * CUBE_FACE_SIZE, row - CUBE_FACE_SIZE, Direction.DOWN
        elif CUBE_FACE_SIZE <= row < 2 * CUBE_FACE_SIZE and col == 2 * CUBE_FACE_SIZE - 1 and d == Direction.RIGHT:
            return CUBE_FACE_SIZE - 1, (2 * CUBE_FACE_SIZE) + (row - CUBE_FACE_SIZE), Direction.UP
        elif row == 2 * CUBE_FACE_SIZE and 0 <= col < CUBE_FACE_SIZE and d == Direction.UP:
            return CUBE_FACE_SIZE + col, CUBE_FACE_SIZE, Direction.RIGHT
        elif 2 * CUBE_FACE_SIZE <= row < 3 * CUBE_FACE_SIZE and col == 0 and d == Direction.LEFT:
            return (3 * CUBE_FACE_SIZE - 1) - row, CUBE_FACE_SIZE, Direction.RIGHT
        elif 2 * CUBE_FACE_SIZE <= row < 3 * CUBE_FACE_SIZE and col == 2 * CUBE_FACE_SIZE - 1 and d == Direction.RIGHT:
            return (3 * CUBE_FACE_SIZE - 1) - row, 3 * CUBE_FACE_SIZE - 1, Direction.LEFT
        elif row == 3 * CUBE_FACE_SIZE - 1 and CUBE_FACE_SIZE <= col < 2 * CUBE_FACE_SIZE and d == Direction.DOWN:
            return (3 * CUBE_FACE_SIZE) + (col - CUBE_FACE_SIZE), CUBE_FACE_SIZE - 1, Direction.LEFT
        elif 3 * CUBE_FACE_SIZE <= row < 4 * CUBE_FACE_SIZE and col == 0 and d == Direction.LEFT:
            return 0, CUBE_FACE_SIZE + (row - 3 * CUBE_FACE_SIZE), Direction.DOWN
        elif 3 * CUBE_FACE_SIZE <= row < 4 * CUBE_FACE_SIZE and col == CUBE_FACE_SIZE - 1 and d == Direction.RIGHT:
            return 3 * CUBE_FACE_SIZE - 1, CUBE_FACE_SIZE + (row - 3 * CUBE_FACE_SIZE), Direction.UP
        elif row == 4 * CUBE_FACE_SIZE - 1 and 0 <= col < CUBE_FACE_SIZE and d == Direction.DOWN:
            return 0, (2 * CUBE_FACE_SIZE) + col, Direction.DOWN
        else:
            match d:
                case Direction.RIGHT:
                    return row, col + 1, d
                case Direction.DOWN:
                    return row + 1, col, d
                case Direction.LEFT:
                    return row, col - 1, d
                case Direction.UP:
                    return row - 1, col, d
                case _:
                    raise ValueError(f"unexpected direction enum: {d}")


def main2(maze: List[str], instructions: List[str]) -> int:
    cube = CubeMaze(maze)
    row = 0
    col = maze[row].index(OPEN)
    d = Direction.RIGHT
    for step in instructions:
        if step == CLOCKWISE:
            d = rot_clockwise(d)
        elif step == COUNTER_CLOCKWISE:
            d = rot_counter_clockwise(d)
        else:  # int
            n_moves = int(step)
            for _ in range(n_moves):
                next_row, next_col, next_d = cube.cube_step(row, col, d)
                # check the val of the next spot
                if maze[next_row][next_col] == OPEN:
                    row = next_row
                    col = next_col
                    d = next_d
                elif maze[next_row][next_col] == WALL:
                    break  # no more moves in this direction
                else:
                    raise ValueError(f"expected open or wall, but found {repr(maze[next_row][next_col])}")
    return (1000 * (row + 1)) + (4 * (col + 1)) + d


if __name__ == "__main__":
    with open(INPUT_PATH, "r", encoding=UTF_8) as f:
        maze_, instructions_ = f.read().split("\n\n")
    maze_ = maze_.split("\n")
    maze_width = max(len(row_) for row_ in maze_)
    maze_ = [
        row_ + (" " * (maze_width - len(row_)))
        for row_ in maze_
    ]
    instructions_ = re.findall(r"\d+|[LR]", instructions_.strip())
    ans = main(maze_, instructions_)
    print("part 1:", ans)
    ans = main2(maze_, instructions_)
    print("part 2:", ans)
