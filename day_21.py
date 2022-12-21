import copy
from pathlib import Path
from typing import Dict, List, Tuple, Union

from constants import INPUTS_DIR, UTF_8

INPUT_PATH = Path(INPUTS_DIR) / "day-21.txt"
# INPUT_PATH = Path(INPUTS_DIR) / "example.txt"

ROOT = "root"
HUMAN = "humn"


def parse(lines: List[str]) -> Dict[str, Union[int, Tuple[str, str, str]]]:
    to_return = {}
    for line in lines:
        this_id, val = line.split(":")
        val = val.strip()
        try:
            val_int = int(val)
            to_return[this_id] = val_int
        except ValueError:  # not an int; must be an expression
            to_return[this_id] = tuple(val.split())
    return to_return


def dfs_calc(data: Dict[str, Union[int, Tuple[str, str, str]]], cur: str, cache: Dict[str, int]) -> int:
    val = data[cur]
    if isinstance(val, int):
        # just use the given value
        to_return = val
    elif isinstance(val, tuple):
        # recursively calculate values for left and right
        left_id, op, right_id = val
        left_val = dfs_calc(data, left_id, cache)
        right_val = dfs_calc(data, right_id, cache)
        # put the values together according to the given expression
        match op:
            case "+":
                new_val = left_val + right_val
            case "*":
                new_val = left_val * right_val
            case "-":
                new_val = left_val - right_val
            case "/":
                new_val = left_val // right_val
            case _:
                raise ValueError(f"unknown operator: {op}")
        to_return = new_val
    else:
        raise TypeError(f"unknown type: {type(val).__name__}")
    # put the new value in the cache, then return it
    cache[cur] = to_return
    return to_return


def main1(data: Dict[str, Union[int, Tuple[str, str, str]]]) -> Tuple[int, Dict[str, int]]:
    cache = {}  # gets filled by dfs_calc
    answer = dfs_calc(data, ROOT, cache)
    return answer, cache


def dfs_calc_inverse(
        data: Dict[str, Union[int, Tuple[str, str, str]]],
        cache: Dict[str, int],
        cur: str,
        target: int,
) -> int:
    val = data[cur]
    if val is None:
        # we got down to the value we're solving for
        return target  # cascades upward
    if not isinstance(val, tuple):
        raise TypeError("algorithm error: didn't get tuple")
    left_id, op, right_id = val
    # figure out 'target', which is the expected value of one of the sub-trees
    if left_id in cache:  # solving for right
        next_cur = right_id
        match op:
            case "+":
                new_target = target - cache[left_id]
            case "*":
                new_target = target // cache[left_id]
            case "-":
                new_target = cache[left_id] - target
            case "/":
                new_target = cache[left_id] // target
            case _:
                raise ValueError(f"unknown operator: {op}")
    elif right_id in cache:  # solving for left
        next_cur = left_id
        match op:
            case "+":
                new_target = target - cache[right_id]
            case "*":
                new_target = target // cache[right_id]
            case "-":
                new_target = target + cache[right_id]
            case "/":
                new_target = target * cache[right_id]
            case _:
                raise ValueError(f"unknown operator: {op}")
    else:
        raise KeyError("algorithm error: neither child in cache")
    # recursion down the tree, then cascade the answer upward
    return dfs_calc_inverse(data, cache, next_cur, new_target)


def main2(data: Dict[str, Union[int, Tuple[str, str, str]]], cache: Dict[str, int]) -> int:
    data = copy.deepcopy(data)
    # calculate which ID it is that depends on each given ID (parent value depends on children values)
    parents = {}
    for parent, children in data.items():
        if isinstance(children, tuple):
            child_a, _, child_b = children
            parents[child_a] = parent
            parents[child_b] = parent
    # modify our data according to the new specs
    root_left, _, root_right = data[ROOT]  # the two expressions we're trying to get to be equal
    del data[ROOT]  # expression no longer valid
    data[HUMAN] = None  # unknown value; what we're solving for
    # clear invalid cache values
    cur = HUMAN
    while cur != ROOT:
        del cache[cur]
        cur = parents[cur]
    del cache[cur]  # root
    # which side has the unknown value, and what should that side's top-level value be?
    if root_right in cache:  # right is known, left has unknown
        target = cache[root_right]
        mystery_root = root_left
    elif root_left in cache:  # left is known, right has unknown
        target = cache[root_left]
        mystery_root = root_right
    else:
        raise KeyError("neither sub-root in cache")
    # start recursively calculating unknown values
    needed_val = dfs_calc_inverse(data, cache, mystery_root, target)
    return needed_val


if __name__ == "__main__":
    with open(INPUT_PATH, "r", encoding=UTF_8) as f:
        lines_ = [line_.strip() for line_ in f.readlines()]
    data_ = parse(lines_)
    ans, cache_ = main1(data_)
    print("part 1:", ans)
    ans = main2(data_, cache_)
    print("part 2:", ans)
