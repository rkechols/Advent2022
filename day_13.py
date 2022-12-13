import copy
import json
from pathlib import Path
from typing import Any, Callable, List, TypeVar, Union, Optional

from constants import INPUTS_DIR, UTF_8

Packet = List[Union[int, List]]

INPUT_PATH = Path(INPUTS_DIR) / "day-13.txt"
# INPUT_PATH = Path(INPUTS_DIR) / "example.txt"

MARKER_A = [[2]]
MARKER_B = [[6]]


def _compare_sub_packets(left: Union[int, List], right: Union[int, List]) -> Optional[bool]:
    if isinstance(left, int):
        if isinstance(right, int):
            if left < right:
                return True
            elif left > right:
                return False
            else:
                return None
        elif isinstance(right, list):
            return _compare_sub_packets([left], right)
        else:
            raise TypeError(f"unexpected type of right: {type(right)}")
    elif isinstance(left, list):
        if isinstance(right, int):
            return _compare_sub_packets(left, [right])
        elif isinstance(right, list):
            n_left = len(left)
            n_right = len(right)
            for i in range(min(n_left, n_right)):
                in_order = _compare_sub_packets(left[i], right[i])
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


def compare_packets(left: Packet, right: Packet) -> bool:
    to_return = _compare_sub_packets(left, right)
    if to_return is None:
        raise ValueError("could not determine relative order")
    return to_return


def main1(packets: List[Packet]) -> int:
    pair_index_sum = 0
    for i in range(0, len(packets), 2):
        left = packets[i]
        right = packets[i + 1]
        if compare_packets(left, right):
            pair_index_sum += ((i // 2) + 1)
    return pair_index_sum


# QUICKSORT - start


T = TypeVar("T")
Comparator = Callable[[T, T], bool]


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


def _partition(data: List[T], start: int, end: int, comparator: Comparator) -> int:
    """
    Within the specified section of a list, sift values to be correctly above and
    below some pivot value (i.e. "partition" it). Return the index of that pivot.
    (The whole list is passed with bounding indices to avoid unnecessary copying)

    Parameters
    ----------
    data: List[T]
        the whole list of values
    start: int
        the index of the first element in the section being partitioned
    end: int
        the index that is 1 after the last element in the section being partitioned
    comparator: Callable[[T, T], bool]
        see docstring of function `quick_sort`

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
        if not comparator(data[index1], data[index2]):
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
        if not comparator(data[i], pivot_value):  # wrong order
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


def _quick_sort_recursive(data: List[T], start: int, end: int, comparator: Comparator):
    """
    Perform quick sort in-place on a section of the list.
    (The whole list is passed with bounding indices to avoid unnecessary copying)

    Parameters
    ----------
    data: List[T]
        the whole list of values being sorted
    start: int
        the index of the first element in the section being sorted
    end: int
        the index that is 1 after the last element in the section being sorted
        (note that `data[start:end]` would return the section in question)
    comparator: Callable[[T, T], bool]
        see docstring of function `quick_sort`

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
        if not comparator(data[index1], data[index2]):
            _swap(data, index1, index2)
        # else:  # no change needed
        return
    # else:  # recursive case:
    pivot_index = _partition(data, start, end, comparator)  # sift values to be below/above some "pivot"
    _quick_sort_recursive(data, start, pivot_index, comparator)  # recursively sort below the pivot
    _quick_sort_recursive(data, pivot_index + 1, end, comparator)  # recursively sort above the pivot


def quick_sort(data: List[T], *, comparator: Comparator = (lambda a, b: a <= b)) -> List[T]:
    """
    Sort the given list of values in-place using the "quick sort" algorithm.

    Parameters
    ----------
    data: List[T]
        the list of values to be sorted
    comparator: Callable[[T, T], bool]
        function used to determine if a pair of values is correctly in order.
        The function should return `True` if the values are given in the correct order (should be left as they are),
        and should return `False` if the values are in the incorrect order and should be swapped.

    Returns
    -------
    List[T]
        `data`, the same list as was passed in.
        Note that `data` is edited in-place by this function;
        returning here is simply for chaining convenience.
    """
    _quick_sort_recursive(data, 0, len(data), comparator)
    return data


# QUICKSORT - end


def main2(packets: List[Packet]) -> int:
    packets = copy.deepcopy(packets)
    packets += [MARKER_A, MARKER_B]
    quick_sort(packets, comparator=compare_packets)
    a = 1 + packets.index(MARKER_A)
    b = 1 + packets.index(MARKER_B)
    return a * b


if __name__ == "__main__":
    with open(INPUT_PATH, "r", encoding=UTF_8) as f:
        lines_ = [line_.strip() for line_ in f.readlines()]
    packets_ = [json.loads(line_) for line_ in lines_ if line_ != ""]
    ans = main1(packets_)
    print("part 1:", ans)
    ans = main2(packets_)
    print("part 2:", ans)
