from pathlib import Path

from constants import INPUTS_DIR, UTF_8

INPUT_PATH = Path(INPUTS_DIR) / "day-06.txt"
# INPUT_PATH = Path(INPUTS_DIR) / "example.txt"


def main(s: str, k: int) -> int:
    for i in range(len(s) - k):
        if len(set(s[i:(i + k)])) == k:
            return i + k
    raise ValueError("no answer found")


if __name__ == "__main__":
    with open(INPUT_PATH, "r", encoding=UTF_8) as f:
        data = f.read().strip()
    ans = main(data, 4)
    print("4 unique:", ans)
    ans = main(data, 14)
    print("14 unique:", ans)
