import copy
import re
from collections import deque
from functools import reduce
from pathlib import Path
from typing import Callable, List, Tuple

from constants import INPUTS_DIR, UTF_8

INPUT_PATH = Path(INPUTS_DIR) / "day-11.txt"
# INPUT_PATH = Path(INPUTS_DIR) / "example.txt"


MONKEY_RE = re.compile(r"Monkey (\d+):")
OPERATION_RE = re.compile(r"new = old ([+*]) (.+)")
DIVISION_RE = re.compile(r"Test: divisible by (\d+)")
TRUE_RE = re.compile(r"If true: throw to monkey (\d+)")
FALSE_RE = re.compile(r"If false: throw to monkey (\d+)")


OperationSpec = Tuple[str, str]


def parse_operation(operation_spec: OperationSpec) -> Callable[[int], int]:
    op, num = operation_spec
    if op == "+":
        if num == "old":
            return lambda old: old + old
        else:
            return lambda old: old + int(num)
    elif op == "*":
        if num == "old":
            return lambda old: old * old
        else:
            return lambda old: old * int(num)
    else:
        raise ValueError(f"Bad operator: {op}")


class Monkey:
    def __init__(self, items: List[int], operation_spec: OperationSpec, div_test: int, true_dest: int, false_dest: int):
        self._items = deque(items)
        self._operation = parse_operation(operation_spec)
        self._div_test = div_test
        self._true_dest = true_dest
        self._false_dest = false_dest

    @property
    def n_items(self) -> int:
        return len(self._items)

    @property
    def divisor(self) -> int:
        return self._div_test

    def pop_item(self) -> int:
        return self._items.popleft()

    def catch_item(self, item: int):
        self._items.append(item)

    def do_operation(self, item: int) -> int:
        return self._operation(item)

    def get_dest(self, item: int) -> int:
        if item % self._div_test == 0:
            return self._true_dest
        else:
            return self._false_dest


def parse(data: str) -> List[Monkey]:
    monkey_blocks = data.split("\n\n")
    to_return = []
    next_i = 0
    for monkey_block in monkey_blocks:
        monkey_lines = monkey_block.split("\n")
        num = int(MONKEY_RE.fullmatch(monkey_lines[0].strip()).group(1))
        if num != next_i:
            raise ValueError(f"wrong order of monkeys! expected {next_i} but got {num}")
        next_i += 1
        starting_items = list(map(int, monkey_lines[1].split(":")[1].strip().split(", ")))
        op, op_num = OPERATION_RE.fullmatch(monkey_lines[2].split(":")[1].strip()).groups()
        division_test = int(DIVISION_RE.fullmatch(monkey_lines[3].strip()).group(1))
        true_dest = int(TRUE_RE.fullmatch(monkey_lines[4].strip()).group(1))
        false_dest = int(FALSE_RE.fullmatch(monkey_lines[5].strip()).group(1))
        monkey = Monkey(
            starting_items,
            (op, op_num),
            division_test,
            true_dest,
            false_dest,
        )
        to_return.append(monkey)
    return to_return


def main(monkeys: List[Monkey], *, n_rounds: int = 20, reduction: Callable[[int], int]) -> int:
    monkeys = copy.deepcopy(monkeys)
    inspect_counts = [0 for _ in range(len(monkeys))]
    for _ in range(n_rounds):  # round
        for i, monkey in enumerate(monkeys):
            while monkey.n_items > 0:
                item = monkey.pop_item()
                item = monkey.do_operation(item)
                inspect_counts[i] += 1
                item = reduction(item)
                dest = monkey.get_dest(item)
                monkeys[dest].catch_item(item)
    inspect_sorted = sorted(inspect_counts, reverse=True)
    a, b = inspect_sorted[:2]
    return a * b


if __name__ == "__main__":
    with open(INPUT_PATH, "r", encoding=UTF_8) as f:
        raw = f.read().strip()
    monkeys_ = parse(raw)
    ans = main(monkeys_, n_rounds=20, reduction=lambda x: x // 3)
    print("part 1:", ans)
    mod_n = reduce((lambda x, y: x * y), (m.divisor for m in monkeys_))
    ans = main(monkeys_, n_rounds=10000, reduction=lambda x: x % mod_n)
    print("part 2:", ans)
