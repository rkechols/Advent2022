import json
from pathlib import Path
from typing import Any, List, Union, Optional

from constants import INPUTS_DIR, UTF_8

INPUT_PATH = Path(INPUTS_DIR) / "day-13.txt"
# INPUT_PATH = Path(INPUTS_DIR) / "example.txt"


Packet = Union[int, List]


def compare(left: Union[int, List], right: Union[int, List]) -> Optional[bool]:
    if isinstance(left, int):
        if isinstance(right, int):
            if left < right:
                return True
            elif left > right:
                return False
            else:
                return None
        elif isinstance(right, list):
            return compare([left], right)
        else:
            raise TypeError(f"unexpected type of right: {type(right)}")
    elif isinstance(left, list):
        if isinstance(right, int):
            return compare(left, [right])
        elif isinstance(right, list):
            n_left = len(left)
            n_right = len(right)
            for i in range(min(n_left, n_right)):
                in_order = compare(left[i], right[i])
                if in_order is not None:
                    return in_order
            if n_left < n_right:
                return True
            elif n_left > n_right:
                return False
            else:
                return None
        else:
            raise TypeError(f"unexpected type of right: {type(right)}")
    else:
        raise TypeError(f"unexpected type of left: {type(left)}")


def main1(lines: List[str]) -> int:
    good_sum = 0
    n_pairs = (len(lines) + 1) // 3
    for i in range(n_pairs):
        left = json.loads(lines[3 * i])
        right = json.loads(lines[(3 * i) + 1])
        in_order = compare(left, right)
        if in_order is None:
            raise ValueError(None)
        if in_order:
            good_sum += (i + 1)
    return good_sum


# QUICKSORT - start


def _swap(data: List[Any], index1: int, index2: int):
    """
    Swaps two elements of a list, as specified by index.
    List is edited in-place.

    Parameters
    ----------
    data: List[Any]
        the list containing elements to be swapped
    index1: int
        the index of one of the elements to be swapped
    index2: int
        the index of the other of the elements to be swapped

    Returns
    -------
    None
    """
    if index1 == index2:
        return  # no point in doing anything
    temp = data[index1]
    data[index1] = data[index2]
    data[index2] = temp


def _partition(data: List[Packet], start: int, end: int) -> int:
    """
    Within the specified section of a list, sift values to be correctly above and
    below some pivot value (i.e. "partition" it). Return the index of that pivot.
    (The whole list is passed with bounding indices to avoid unnecessary copying)

    Parameters
    ----------
    data: List[Packet]
        the whole list of values
    start: int
        the index of the first element in the section being partitioned
    end: int
        the index that is 1 after the last element in the section being partitioned

    Returns
    -------
    int
        the index of the pivot element, as the list is when the function returns

    Raises
    ------
    ValueError
        if start < 0, or
        if end > len(data), or
        if end <= start
    """
    # validate args
    if start < 0:
        raise ValueError(f"start (which was {start}) must be >= 0")
    n = len(data)
    if end > n:
        raise ValueError(f"end (which was {end}) must be < len(data) (which is {n})")
    section_len = end - start
    if section_len <= 0:
        raise ValueError(f"start (which was {start}) must be less than end (which was {end})")
    # check some (valid) base cases (even though _quick_sort_recursive should stop these from getting here)
    elif section_len == 1:  # this section is too small for partition to mean anything
        return start
    elif section_len == 2:
        index1 = start
        index2 = start + 1
        in_order = compare(data[index1], data[index2])
        if in_order is None:
            raise ValueError(None)
        if not in_order:
            _swap(data, index1, index2)
            return index1
        else:  # no change needed
            return index2
    # else:  # do the normal thing
    # swap all the highs up to the end of the list
    pivot_index_initial = end - 1
    pivot_value = data[pivot_index_initial]
    next_high_index = end - 2  # keeps track of where to put the next "high" we find
    i = start
    while i <= next_high_index:  # no need to re-look through all of our high numbers
        in_order = compare(data[i], pivot_value)
        if in_order is None:
            raise ValueError(None)
        if not in_order:
            # swap this to the end (just before all the other highs we've put there)
            _swap(data, next_high_index, i)
            next_high_index -= 1
            # don't increment i; we need to check the new number that got put here
        else:  # all is well; move along
            i += 1
    # swap the pivot with the first high, so it's between the highs and lows
    pivot_index_final = next_high_index + 1
    _swap(data, pivot_index_final, pivot_index_initial)
    # return the index of the pivot, as the list now is
    return pivot_index_final


def _quick_sort_recursive(data: List[Packet], start: int, end: int):
    """
    Perform quick sort in-place on a section of the list.
    (The whole list is passed with bounding indices to avoid unnecessary copying)

    Parameters
    ----------
    data: List[Packet]
        the whole list of values being sorted
    start: int
        the index of the first element in the section being sorted
    end: int
        the index that is 1 after the last element in the section being sorted
        (note that `data[start:end]` would return the section in question)

    Returns
    -------
    None

    Raises
    ------
    ValueError
        if start < 0, or
        if end > len(data), or
        if end < start
    """
    # validate args
    if start < 0:
        raise ValueError(f"start (which was {start}) must be >= 0")
    n = len(data)
    if end > n:
        raise ValueError(f"end (which was {end}) must be < len(data) (which is {n})")
    section_len = end - start
    if section_len < 0:
        raise ValueError(f"start (which was {start}) must be less than or equal to end (which was {end})")
    # base cases to terminate recursion
    elif section_len <= 1:  # this section is too small for sort to mean anything
        return
    elif section_len == 2:  # just do a singular check, swap if needed
        index1 = start
        index2 = start + 1
        out = compare(data[index1], data[index2])
        if out is None:
            raise ValueError(None)
        if not out:
            _swap(data, index1, index2)
        # else:  # no change needed
        return
    # else:  # recursive case:
    pivot_index = _partition(data, start, end)  # sift values to be below/above some "pivot"
    _quick_sort_recursive(data, start, pivot_index)  # recursively sort below the pivot
    _quick_sort_recursive(data, pivot_index + 1, end)  # recursively sort above the pivot


def quick_sort(data: List[Packet]):
    """
    Sort the given list in-place using the "quick sort" algorithm.

    Parameters
    ----------
    data: List[Packet]
        the list of values to be sorted

    Returns
    -------
    None
    """
    _quick_sort_recursive(data, 0, len(data))


# QUICKSORT - end


def main2(lines: List[str]) -> int:
    lines = [json.loads(lines[i]) for i in range(len(lines)) if (i % 3 != 2)]
    lines += [[[2]], [[6]]]
    quick_sort(lines)
    a = 1 + lines.index([[2]])
    b = 1 + lines.index([[6]])
    return a * b


if __name__ == "__main__":
    with open(INPUT_PATH, "r", encoding=UTF_8) as f:
        lines_ = [line_.strip() for line_ in f.readlines()]
    ans = main1(lines_)
    print("part 1:", ans)
    ans = main2(lines_)
    print("part 2:", ans)
