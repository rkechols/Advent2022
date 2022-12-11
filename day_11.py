import copy
from functools import reduce
from tqdm import tqdm
import re
from pathlib import Path
from collections import deque
from typing import List, Tuple, Type, Union

from constants import INPUTS_DIR, UTF_8

INPUT_PATH = Path(INPUTS_DIR) / "day-11.txt"
# INPUT_PATH = Path(INPUTS_DIR) / "example.txt"


MONKEY_RE = re.compile(r"Monkey (\d+):")
DIVISION_RE = re.compile(r"Test: divisible by (\d+)")
TRUE_RE = re.compile(r"If true: throw to monkey (\d+)")
FALSE_RE = re.compile(r"If false: throw to monkey (\d+)")
OPERATION_RE = re.compile(r"new = old ([+*]) (.+)")


class Monkey:
    def __init__(self, num: int, items: List[int], operation: Tuple[str, str], div_test: int, true_dest: int, false_dest: int):
        self.num = num
        self.items = deque(items)
        self.operation = operation
        self.div_test = div_test
        self.true_dest = true_dest
        self.false_dest = false_dest

    def __repr__(self):
        return f"Monkey(num_items={len(self.items)})"


def do_operation(old: int, operation: Tuple[str, str]) -> int:
    op, num = operation
    if num == "old":
        num = old
    else:
        num = int(num)
    if op == "+":
        return old + num
    elif op == "*":
        return old * num
    else:
        raise ValueError(f"Bad operator: {op}")


def parse(data: str) -> List:
    monkeys = data.split("\n\n")
    to_return = []
    next_i = 0
    for monkey in monkeys:
        monkey_lines = monkey.split("\n")
        num = int(MONKEY_RE.fullmatch(monkey_lines[0].strip()).group(1))
        if num != next_i:
            raise ValueError(f"wrong order of monkeys! expected {next_i} but got {num}")
        next_i += 1
        starting_items = list(map(int, monkey_lines[1].split(":")[1].strip().split(", ")))
        op, op_num = OPERATION_RE.fullmatch(monkey_lines[2].split(":")[1].strip()).groups()
        division_test = int(DIVISION_RE.fullmatch(monkey_lines[3].strip()).group(1))
        true_dest = int(TRUE_RE.fullmatch(monkey_lines[4].strip()).group(1))
        false_dest = int(FALSE_RE.fullmatch(monkey_lines[5].strip()).group(1))
        m = Monkey(
            num,
            starting_items,
            (op, op_num),
            division_test,
            true_dest,
            false_dest,
        )
        to_return.append(m)
    return to_return


def main(monkeys: List[Monkey], n_rounds: int = 20) -> int:
    monkeys = copy.deepcopy(monkeys)
    inspect_counts = [0 for _ in range(len(monkeys))]
    for _ in tqdm(range(n_rounds)):  # round
        for i, monkey in enumerate(monkeys):
            while len(monkey.items) > 0:
                item = monkey.items.popleft()
                item = do_operation(item, monkey.operation)
                inspect_counts[i] += 1
                item = item // 3
                if item % monkey.div_test == 0:
                    dest = monkey.true_dest
                else:
                    dest = monkey.false_dest
                monkeys[dest].items.append(item)
    inspect_sorted = sorted(inspect_counts, reverse=True)
    a, b = inspect_sorted[:2]
    return a * b


def main2(monkeys: List[Monkey], n_rounds: int = 20) -> int:
    monkeys = copy.deepcopy(monkeys)
    inspect_counts = [0 for _ in range(len(monkeys))]
    for _ in tqdm(range(n_rounds)):  # round
        for i, monkey in enumerate(monkeys):
            while len(monkey.items) > 0:
                item = monkey.items.popleft()
                item = do_operation(item, monkey.operation)
                inspect_counts[i] += 1
                if item % monkey.div_test == 0:
                    dest = monkey.true_dest
                else:
                    dest = monkey.false_dest
                monkeys[dest].items.append(item)
    inspect_sorted = sorted(inspect_counts, reverse=True)
    a, b = inspect_sorted[:2]
    return a * b


if __name__ == "__main__":
    with open(INPUT_PATH, "r", encoding=UTF_8) as f:
        raw = f.read().strip()
    data_ = parse(raw)
    ans = main(data_, n_rounds=20)
    print("part 1:", ans)
    ans = main2(data_, n_rounds=10000)
    print("part 2:", ans)
