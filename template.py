from pathlib import Path
from typing import List

from constants import INPUTS_DIR, UTF_8


INPUT_PATH = Path(INPUTS_DIR) / "day-00.txt"


def main(lines: List[str]):
    pass  # TODO


if __name__ == "__main__":
    with open(INPUT_PATH, "r", encoding=UTF_8) as f:
        lines_ = f.readlines()
    ans = main(lines_)
    print(ans)
