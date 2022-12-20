from pathlib import Path
from typing import List, TypedDict

from tqdm import tqdm

from constants import INPUTS_DIR, UTF_8

INPUT_PATH = Path(INPUTS_DIR) / "day-20.txt"
# INPUT_PATH = Path(INPUTS_DIR) / "example.txt"


class Datum(TypedDict):
    index: int
    val: int


def get_ordered(mixer: List[Datum]) -> List[int]:
    mixed: List[int] = [None for _ in range(len(mixer))]
    for d in mixer:
        if mixed[d["index"]] is not None:
            raise ValueError("multiple assignment error")
        mixed[d["index"]] = d["val"]
    return mixed


def move_forward(mixer: List[Datum], d: Datum, n_moves: int):
    index = d["index"]
    target = index + n_moves
    if target >= len(mixer):
        raise ValueError("`move_forward` is not prepared to wrap around")
    for other_d in mixer:
        other_index = other_d["index"]
        if index < other_index <= target:
            other_d["index"] -= 1
    d["index"] = target


def move_backward(mixer: List[Datum], d: Datum, n_moves: int):
    index = d["index"]
    target = index - n_moves
    if target < 0:
        raise ValueError("`move_backward` is not prepared to wrap around")
    for other_d in mixer:
        other_index = other_d["index"]
        if index > other_index >= target:
            other_d["index"] += 1
    d["index"] = target


def main(data: List[int], *, n_rounds: int = 1) -> int:
    n = len(data)
    mixer = list(({"val": val, "index": i} for i, val in enumerate(data)))
    for _ in tqdm(range(n_rounds)):
        for d in mixer:
            val = d["val"]
            index = d["index"]
            if val == 0:
                continue
            elif val > 0:  # forward
                val_mod = val % (n - 1)
                if index + val_mod >= n:  # overflow
                    move_backward(mixer, d, (n - val_mod - 1))
                else:
                    move_forward(mixer, d, val_mod)
            else:  # val < 0:  # backward
                val_mod = -val % (n - 1)
                if index - val_mod < 0:  # underflow
                    move_forward(mixer, d, (n - val_mod - 1))
                else:
                    move_backward(mixer, d, val_mod)
    # make actual result list
    mixed = get_ordered(mixer)
    # find 0
    index_0 = mixed.index(0)
    return sum(
        mixed[(index_0 + shift) % n]
        for shift in (1000, 2000, 3000)
    )


if __name__ == "__main__":
    with open(INPUT_PATH, "r", encoding=UTF_8) as f:
        data_ = [int(line_.strip()) for line_ in f.readlines()]
    ans = main(data_, n_rounds=1)
    print("part 1:", ans)
    data_2 = [
        num * 811589153
        for num in data_
    ]
    ans = main(data_2, n_rounds=10)
    print("part 2:", ans)
