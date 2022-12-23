import sys
from collections import Counter
from pathlib import Path
from typing import List, Set, Tuple, Iterable

from constants import INPUTS_DIR, UTF_8

Point = Tuple[int, int]

INPUT_PATH = Path(INPUTS_DIR) / "day-23.txt"
# INPUT_PATH = Path(INPUTS_DIR) / "example.txt"


ELF = "#"
EMPTY = "."

DIRECTION_ORDER = ["N", "S", "W", "E"]
N_DIRECTIONS = len(DIRECTION_ORDER)


def parse(lines: List[str]) -> Set[Point]:
    to_return = set()
    for i, line in enumerate(lines):
        for j, symbol in enumerate(line):
            if symbol == ELF:
                to_return.add((i, j))
    return to_return


def get_all_neighbors(pos: Point) -> Iterable[Point]:
    for i_shift in (-1, 0, 1):
        for j_shift in (-1, 0, 1):
            if i_shift == 0 and j_shift == 0:
                continue  # don't produce the center
            yield pos[0] + i_shift, pos[1] + j_shift


def get_dir_neighbors(pos: Point, direction: str) -> Iterable[Point]:
    match direction:
        case "N":
            new_row = pos[0] - 1
            for col_shift in (-1, 0, 1):
                yield new_row, pos[1] + col_shift
        case "S":
            new_row = pos[0] + 1
            for col_shift in (-1, 0, 1):
                yield new_row, pos[1] + col_shift
        case "W":
            new_col = pos[1] - 1
            for row_shift in (-1, 0, 1):
                yield pos[0] + row_shift, new_col
        case "E":
            new_col = pos[1] + 1
            for row_shift in (-1, 0, 1):
                yield pos[0] + row_shift, new_col
        case _:
            raise ValueError(f"Unknown direction: {direction}")


def main(elves: Set[Point], *, n_rounds: int = None) -> int:
    i_dir = 0
    current_round = 0
    while True:
        current_round += 1
        guaranteed = {}
        proposals = {}
        no_move_needed = True
        for elf in elves:
            # do nothing if no neighbors
            if all(neighbor not in elves for neighbor in get_all_neighbors(elf)):
                guaranteed[elf] = elf
                continue
            # else: not yet sufficiently spaced out
            no_move_needed = False
            # propose a direction with no other elves
            for i_dir_shift in range(N_DIRECTIONS):  # iterate across preferences
                direction = DIRECTION_ORDER[(i_dir + i_dir_shift) % N_DIRECTIONS]
                # check if this direction is completely clear of other elves
                if any(neighbor in elves for neighbor in get_dir_neighbors(elf, direction)):
                    continue
                # the proposed position
                match direction:
                    case "N":
                        proposed = elf[0] - 1, elf[1]
                    case "S":
                        proposed = elf[0] + 1, elf[1]
                    case "W":
                        proposed = elf[0], elf[1] - 1
                    case "E":
                        proposed = elf[0], elf[1] + 1
                    case _:
                        raise ValueError(f"Unknown direction: {direction}")
                proposals[elf] = proposed
                break
            else:  # no proposal/movement possible; stay here
                guaranteed[elf] = elf
        # all elves are sufficiently spaced out
        if no_move_needed:
            print(f"Elves sufficiently spaced out after round #{current_round}", file=sys.stderr)
            break
        # check overlap in proposals
        proposal_counts = Counter(proposals.values())
        for proposer, proposed in proposals.items():
            if proposal_counts[proposed] <= 1:  # no competition for the spot
                guaranteed[proposer] = proposed  # accept proposal
            else:
                guaranteed[proposer] = proposer  # stay put
        # update elf positions
        elves = set(guaranteed.values())
        # change direction preference
        i_dir = (i_dir + 1) % N_DIRECTIONS
        # check early termination
        if n_rounds is not None and current_round >= n_rounds:
            print(f"Stopped early, after {n_rounds} round(s)", file=sys.stderr)
            break
    # calculate number of empty spots in the smallest enclosing rectangle
    i_min = min(elf[0] for elf in elves)
    i_max = max(elf[0] for elf in elves)
    j_min = min(elf[1] for elf in elves)
    j_max = max(elf[1] for elf in elves)
    n_cells = (1 + i_max - i_min) * (1 + j_max - j_min)
    n_empty = n_cells - len(elves)
    return n_empty


if __name__ == "__main__":
    with open(INPUT_PATH, "r", encoding=UTF_8) as f:
        lines_ = [line_.strip() for line_ in f.readlines()]
    elves_ = parse(lines_)
    ans = main(elves_, n_rounds=10)
    print("part 1:", ans)
    ans = main(elves_)
    print("part 2:", ans)
