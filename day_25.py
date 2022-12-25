from pathlib import Path
from typing import List

from constants import INPUTS_DIR, UTF_8

INPUT_PATH = Path(INPUTS_DIR) / "day-25.txt"
# INPUT_PATH = Path(INPUTS_DIR) / "example.txt"


BASE = 5
DIGIT_TO_VAL = {
    "=": -2,
    "-": -1,
    "0": 0,
    "1": 1,
    "2": 2,
}
VAL_TO_DIGIT = {
    val: digit
    for digit, val in DIGIT_TO_VAL.items()
}


def snafu_to_decimal(snafu: str) -> int:
    total = 0
    for power, digit in enumerate(reversed(snafu)):
        total += DIGIT_TO_VAL[digit] * (5 ** power)
    return total


def decimal_to_snafu(num: int) -> str:
    # get num in normal base 5
    values = []
    while num > 0:
        val = num % BASE
        values.append(val)
        num = num // BASE
    # adjust to fit snafu
    place = 0
    while place < len(values):
        if values[place] not in VAL_TO_DIGIT:
            values[place] -= BASE
            try:
                values[place + 1] += 1
            except IndexError:
                values[place + 1] = 1
        place += 1
    # print as snafu number
    digits = [
        VAL_TO_DIGIT[value]
        for value in reversed(values)
    ]
    return "".join(digits)


def main(lines: List[str]) -> str:
    total = 0
    for line in lines:
        dec_val = snafu_to_decimal(line)
        total += dec_val
    return decimal_to_snafu(total)


if __name__ == "__main__":
    with open(INPUT_PATH, "r", encoding=UTF_8) as f:
        lines_ = [line_.strip() for line_ in f.readlines()]
    ans = main(lines_)
    print(ans)
