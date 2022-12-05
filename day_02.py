from pathlib import Path
from typing import List, Tuple, cast

from constants import INPUTS_DIR, UTF_8

INPUT_PATH = Path(INPUTS_DIR) / "day-02.txt"
# INPUT_PATH = Path(INPUTS_DIR) / "example.txt"

ROCK_IN = "A"
PAPER_IN = "B"
SCISSORS_IN = "C"

ROCK_OUT = "X"
PAPER_OUT = "Y"
SCISSORS_OUT = "Z"

NEED_LOSE = "X"
NEED_DRAW = "Y"
NEED_WIN = "Z"

ROCK_SCORE = 1
PAPER_SCORE = 2
SCISSORS_SCORE = 3

SCORE_LOSE = 0
SCORE_DRAW = 3
SCORE_WIN = 6


def main1(lines: List[Tuple[str, str]]) -> int:
    total = 0
    for them, me in lines:
        if me == ROCK_OUT:
            total += ROCK_SCORE
            if them == ROCK_IN:
                total += SCORE_DRAW
            elif them == PAPER_IN:
                total += SCORE_LOSE
            elif them == SCISSORS_IN:
                total += SCORE_WIN
            else:
                raise RuntimeError(f"bad val for 'them' {me=} {them=}")
        elif me == PAPER_OUT:
            total += PAPER_SCORE
            if them == ROCK_IN:
                total += SCORE_WIN
            elif them == PAPER_IN:
                total += SCORE_DRAW
            elif them == SCISSORS_IN:
                total += SCORE_LOSE
            else:
                raise RuntimeError(f"bad val for 'them' {me=} {them=}")
        elif me == SCISSORS_OUT:
            total += SCISSORS_SCORE
            if them == ROCK_IN:
                total += SCORE_LOSE
            elif them == PAPER_IN:
                total += SCORE_WIN
            elif them == SCISSORS_IN:
                total += SCORE_DRAW
            else:
                raise RuntimeError(f"bad val for 'them' {me=} {them=}")
        else:
            raise RuntimeError(f"bad val for 'me' {me=} {them=}")
    return total


def main2(lines: List[Tuple[str, str]]) -> int:
    total = 0
    for them, me in lines:
        if me == NEED_WIN:
            total += SCORE_WIN
            if them == ROCK_IN:
                total += PAPER_SCORE
            elif them == PAPER_IN:
                total += SCISSORS_SCORE
            elif them == SCISSORS_IN:
                total += ROCK_SCORE
            else:
                raise RuntimeError(f"bad val for 'them' {me=} {them=}")
        elif me == NEED_DRAW:
            total += SCORE_DRAW
            if them == ROCK_IN:
                total += ROCK_SCORE
            elif them == PAPER_IN:
                total += PAPER_SCORE
            elif them == SCISSORS_IN:
                total += SCISSORS_SCORE
            else:
                raise RuntimeError(f"bad val for 'them' {me=} {them=}")
        elif me == NEED_LOSE:
            total += SCORE_LOSE
            if them == ROCK_IN:
                total += SCISSORS_SCORE
            elif them == PAPER_IN:
                total += ROCK_SCORE
            elif them == SCISSORS_IN:
                total += PAPER_SCORE
            else:
                raise RuntimeError(f"bad val for 'them' {me=} {them=}")
        else:
            raise RuntimeError(f"bad val for 'me' {me=} {them=}")
    return total


if __name__ == "__main__":
    with open(INPUT_PATH, "r", encoding=UTF_8) as f:
        lines_ = f.readlines()
    lines_ = [
        cast(
            Tuple[str, str],
            tuple(line_.strip().split())
        )
        for line_ in lines_
    ]
    ans = main1(lines_)
    print("part 1:", ans)
    ans = main2(lines_)
    print("part 2:", ans)
