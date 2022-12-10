from pathlib import Path
from typing import List, Tuple

from constants import INPUTS_DIR, UTF_8

N_ROWS = 6
N_COLS = 40


INPUT_PATH = Path(INPUTS_DIR) / "day-10.txt"
# INPUT_PATH = Path(INPUTS_DIR) / "example.txt"


def check_cycle(cycle: int) -> bool:
    return (cycle - 20) % 40 == 0


def cycle_to_row_col(cycle: int) -> Tuple[int, int]:
    cycle = cycle - 1
    row = (cycle // N_COLS) % N_ROWS
    col = cycle % N_COLS
    return row, col


def try_draw(screen: List[List[str]], x: int, cycle: int):
    row, col = cycle_to_row_col(cycle)
    if abs(x - col) <= 1:
        screen[row][col] = "#"


def main(lines: List[str]) -> Tuple[int, List[List[str]]]:
    cycle = 0
    x = 1
    total_strength = 0
    screen = [
        ["." for _ in range(N_COLS)]
        for _ in range(N_ROWS)
    ]
    for line in lines:
        if line == "noop":
            cycle += 1
            try_draw(screen, x, cycle)
            if check_cycle(cycle):
                total_strength += cycle * x
        elif line.startswith("addx"):
            for _ in range(2):
                cycle += 1
                try_draw(screen, x, cycle)
                if check_cycle(cycle):
                    total_strength += cycle * x
            x += int(line[5:])
        else:
            raise ValueError(f"bad line: {line}")
    return total_strength, screen


if __name__ == "__main__":
    with open(INPUT_PATH, "r", encoding=UTF_8) as f:
        lines_ = [line_.strip() for line_ in f.readlines()]
    ans, drawing_ = main(lines_)
    print("part 1:", ans)
    print("part 2:")
    for row_ in drawing_:
        print("".join(row_))
