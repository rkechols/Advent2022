from pathlib import Path
from typing import Tuple

import numpy as np

from constants import INPUTS_DIR, UTF_8

INPUT_PATH = Path(INPUTS_DIR) / "day-17.txt"
# INPUT_PATH = Path(INPUTS_DIR) / "example.txt"

LEFT = "<"
RIGHT = ">"
WIDTH = 7
LEFT_START_GAP = 2
BOTTOM_START_GAP = 3

SHAPES = [
    np.array([
        [True, True, True, True]
    ]),
    np.array([
        [False, True, False],
        [True, True, True],
        [False, True, False],
    ]),
    np.array([
        [False, False, True],
        [False, False, True],
        [True, True, True],
    ]),
    np.array([
        [True], [True], [True], [True]
    ]),
    np.array([
        [True, True],
        [True, True],
    ]),
]
N_SHAPES = len(SHAPES)
BIGGEST_SHAPE_HEIGHT = max(a.shape[0] for a in SHAPES)


def has_overlap(canvas: np.ndarray, cur_shape: np.ndarray, bottom_edge: int, h_shift: int) -> bool:
    bottom_edge_real = canvas.shape[0] - bottom_edge
    top_edge_real = bottom_edge_real - cur_shape.shape[0]
    return any(
        canvas[top_edge_real + i, h_shift + j] and cur_shape[i, j]
        for i in range(cur_shape.shape[0] - 1, -1, -1)
        for j in range(cur_shape.shape[1])
    )


def bfs(canvas: np.ndarray) -> int:
    start = (BOTTOM_START_GAP - 1, WIDTH // 2)
    q = {start}
    visited = set()
    deepest = None
    while len(q) > 0:
        new_q = set()
        for loc in q:
            visited.add(loc)
            if deepest is None or loc[0] > deepest:
                deepest = loc[0]
            for shift in [(0, -1), (1, 0), (0, 1)]:
                new_loc = tuple(a + b for a, b in zip(loc, shift))
                try:
                    if (new_loc not in visited) and (not canvas[new_loc]):
                        new_q.add(new_loc)
                except IndexError:
                    pass
        q = new_q
    return deepest


def bool_arr_to_int(arr: np.ndarray) -> int:
    bin_string = "".join("1" if elem else "0" for elem in np.nditer(arr))
    return int(bin_string, 2)


class State:
    def __init__(self, index_instruction: int, n_landed: int, board: np.ndarray, n_trimmed: int):
        self.index_instruction = index_instruction
        self.n_landed = n_landed
        self.board = board
        self.n_trimmed = n_trimmed

    def to_key(self) -> Tuple[int, int, int]:
        return (
            self.index_instruction,
            self.n_landed % N_SHAPES,
            bool_arr_to_int(self.board),
        )


def main(instructions: str, *, n_rocks: int):
    n_instructions = len(instructions)
    canvas = np.zeros((BIGGEST_SHAPE_HEIGHT + BOTTOM_START_GAP, WIDTH), dtype=bool)
    highest = 0
    n_landed = 0
    n_trimmed = 0
    # first rock
    cur_shape = SHAPES[n_landed % N_SHAPES]
    h_shift = LEFT_START_GAP
    bottom_edge = highest + BOTTOM_START_GAP
    # watch for repeats
    state_cache = {}
    cycle_found = False
    # start looping over instructions
    index_instruction = 0
    while True:  # infinite repeats of instruction list
        instruction = instructions[index_instruction]
        # do push
        if instruction == LEFT:
            if h_shift > 0 and not has_overlap(canvas, cur_shape, bottom_edge, h_shift - 1):
                h_shift -= 1
        elif instruction == RIGHT:
            if h_shift < WIDTH - cur_shape.shape[1] \
                    and not has_overlap(canvas, cur_shape, bottom_edge, h_shift + 1):
                h_shift += 1
        else:
            raise ValueError(f"invalid push value: {instruction}")
        # do fall
        if bottom_edge == 0 or has_overlap(canvas, cur_shape, bottom_edge - 1, h_shift):
            # can't fall; land where we are
            bottom_edge_real = canvas.shape[0] - bottom_edge
            top_edge_real = bottom_edge_real - cur_shape.shape[0]
            right_edge = h_shift + cur_shape.shape[1]
            canvas[top_edge_real:bottom_edge_real, h_shift:right_edge] |= cur_shape
            this_top = canvas.shape[0] - top_edge_real
            highest = max(highest, this_top)
            n_landed += 1
            if n_landed == n_rocks:
                return n_trimmed + highest
            # trim if possible
            deepest_reachable = bfs(canvas)
            trim_index = deepest_reachable + 2
            current_trim_size = canvas.shape[0] - trim_index
            if current_trim_size > 0:
                canvas = canvas[:trim_index]
                bottom_edge -= current_trim_size
                highest -= current_trim_size
                n_trimmed += current_trim_size
            # add padding to the top if needed
            n_blank_rows = canvas.shape[0] - highest
            n_blanks_to_add = (BIGGEST_SHAPE_HEIGHT + BOTTOM_START_GAP) - n_blank_rows
            if n_blanks_to_add > 0:
                canvas = np.concatenate([
                    np.zeros((n_blanks_to_add, WIDTH), dtype=bool),
                    canvas,
                ])
            # save state, check if we're in a cycle
            if not cycle_found:
                state = State(
                    index_instruction=index_instruction,
                    n_landed=n_landed,
                    board=canvas,
                    n_trimmed=n_trimmed,
                )
                state_key = state.to_key()
                if state_key in state_cache:  # we have a cycle
                    cycle_found = True
                    prev_state = state_cache[state_key]
                    # what does the cycle pattern look like
                    cycle_start = prev_state.n_landed
                    cycle_length = state.n_landed - prev_state.n_landed
                    n_cycles_complete = (n_rocks - cycle_start) // cycle_length
                    cycle_trim_diff = state.n_trimmed - prev_state.n_trimmed
                    # skip a bunch of steps
                    n_landed = cycle_start + n_cycles_complete * cycle_length
                    n_trimmed = prev_state.n_trimmed + n_cycles_complete * cycle_trim_diff
                else:  # not a repeat
                    state_cache[state_key] = state
            # get a new rock
            cur_shape = SHAPES[n_landed % N_SHAPES]
            h_shift = LEFT_START_GAP
            bottom_edge = highest + BOTTOM_START_GAP
        else:  # normal fall
            bottom_edge -= 1
        # get ready for next instruction
        index_instruction = (index_instruction + 1) % n_instructions


if __name__ == "__main__":
    with open(INPUT_PATH, "r", encoding=UTF_8) as f:
        data_ = f.read().strip()
    ans = main(data_, n_rocks=2022)
    print("part 1:", ans)
    ans = main(data_, n_rocks=1000000000000)
    print("part 2:", ans)
