import copy
import heapq
import re
from pathlib import Path
from typing import List, Dict, Set, Tuple, Optional, Iterable

from constants import INPUTS_DIR, UTF_8

INPUT_PATH = Path(INPUTS_DIR) / "day-16.txt"
# INPUT_PATH = Path(INPUTS_DIR) / "example.txt"

LINE_RE = re.compile(r"Valve (.*) has flow rate=(\d+); tunnels? leads? to valves? (.*)")

START = "AA"
TIME_LIMIT = 26


def parse(lines: List[str]) -> Tuple[Dict[str, int], Dict[str, Set[str]]]:
    flows = {}
    adj = {}
    for line in lines:
        valve, flow, neighbors = LINE_RE.fullmatch(line).groups()
        flow = int(flow)
        neighbors = set(neighbors.split(", "))
        flows[valve] = flow
        adj[valve] = neighbors
    return flows, adj


class PartialSolution:
    __slots__ = "cur1", "cur2", "timer", "flows", "adj", "opened", "unopened", "_score"

    def __init__(self, *, cur1: str, cur2: str, timer: int,
                 flows: Dict[str, int], adj: Dict[str, Set[str]],
                 opened: Dict[str, int], unopened: Set[str]):
        self.cur1 = cur1
        self.cur2 = cur2
        self.timer = timer
        self.flows = flows
        self.adj = adj
        self.opened = opened
        self.unopened = unopened
        # late init:
        self._score: Optional[int] = None

    # def unopened(self) -> Set[str]:
    #     return set(self.flows.keys()) - set(self.opened.keys())

    def score(self) -> int:
        return sum(
            self.flows[valve] * steps_open
            for valve, steps_open in self.opened.items()
        )

    def score_hypothetical(self) -> int:
        if self._score is None:
            so_far = self.score()
            sorted_remaining_flows = sorted(
                (
                    flow
                    for valve in self.unopened
                    if (flow := self.flows[valve]) > 0
                ),
                reverse=True
            )
            # shift1 = -1 if self.can_open(self.cur1) else 0
            shift1 = 0
            hypothetical1 = sum(
                flow * steps_remaining
                for flow, steps_remaining in zip(
                    sorted_remaining_flows[::2],
                    range(self.timer + shift1, 0, -2)
                )
            )
            # shift2 = -1 if self.can_open(self.cur2) else 0
            shift2 = 0
            hypothetical2 = sum(
                flow * steps_remaining
                for flow, steps_remaining in zip(
                    sorted_remaining_flows[1::2],
                    range(self.timer + shift2, 0, -2)
                )
            )
            self._score = so_far + hypothetical1 + hypothetical2
        return self._score

    def score_heap(self) -> int:
        return -1 * self.score_hypothetical() * len(self.opened)

    def is_complete(self) -> bool:
        return self.timer == 0 or all(
            self.flows[valve] == 0
            for valve in self.unopened
        )

    def clone(self) -> 'PartialSolution':
        return PartialSolution(
            cur1=self.cur1,
            cur2=self.cur2,
            timer=self.timer,
            flows=self.flows,
            adj=self.adj,
            opened=copy.copy(self.opened),
            unopened=copy.copy(self.unopened),
        )

    def children1(self, best_score: int) -> Iterable['PartialSolution']:
        to_return = []
        # open this valve
        if self.can_open(self.cur1):
            child = self.clone()
            child.timer -= 1
            child.open(self.cur1)

            score = child.score_hypothetical()
            if score > best_score:

                to_return.append(child)
        # go to each neighbor
        for neighbor in self.adj[self.cur1]:
            child = self.clone()
            child.timer -= 1
            child.move1(neighbor)

            score = child.score_hypothetical()
            if score > best_score:

                to_return.append(child)
        return to_return

    def children2(self) -> Iterable['PartialSolution']:
        to_return = []
        # open this valve
        if self.can_open(self.cur2):
            child = self.clone()
            # child.timer -= 1
            child.open(self.cur2)
            to_return.append(child)
        # go to each neighbor
        for neighbor in self.adj[self.cur2]:
            child = self.clone()
            # child.timer -= 1
            child.move2(neighbor)
            to_return.append(child)
        return to_return

    def children(self, best_score: int) -> Iterable['PartialSolution']:
        to_return = [
            child
            for child_level1 in self.children1(best_score)
            for child in child_level1.children2()
        ]
        return to_return

    def can_open(self, cur: str) -> bool:
        return (cur not in self.opened) and (self.flows[cur] > 0)

    def open(self, cur: str):
        if not self.can_open(cur):
            raise ValueError(f"try to open {cur}, which is already open")
        self.opened[cur] = self.timer
        self.unopened.remove(cur)
        self._score = None

    def move1(self, dest: str):
        self.cur1 = dest
        # self._score = None

    def move2(self, dest: str):
        self.cur2 = dest
        # self._score = None


class HeapElem:
    __slots__ = "val",

    def __init__(self, val: PartialSolution):
        self.val = val

    def __lt__(self, other: 'HeapElem') -> bool:
        return self.val.score_heap() < other.val.score_heap()

    def __gt__(self, other: 'HeapElem') -> bool:
        return self.val.score_heap() > other.val.score_heap()

    def __eq__(self, other: 'HeapElem') -> bool:
        return self.val.score_heap() == other.val.score_heap()


def main(flows: Dict[str, int], adj: Dict[str, Set[str]]) -> int:
    best_score = 1285
    heap = [HeapElem(PartialSolution(
        cur1=START,
        cur2=START,
        timer=TIME_LIMIT,
        flows=flows,
        adj=adj,
        opened={},
        unopened=set(flows.keys()),
    ))]
    while len(heap) > 0:
        state = heapq.heappop(heap).val
        score = state.score_hypothetical()
        if score <= best_score:
            continue
        for possible_child in state.children(best_score):
            if possible_child.is_complete():
                score = possible_child.score()
                best_score = max(best_score, score)
            else:
                score = possible_child.score_hypothetical()
                if score > best_score:
                    heapq.heappush(heap, HeapElem(possible_child))
    return best_score


if __name__ == "__main__":
    with open(INPUT_PATH, "r", encoding=UTF_8) as f:
        lines_ = [line_.strip() for line_ in f.readlines()]
    flows_, adj_ = parse(lines_)
    ans = main(flows_, adj_)
    print("part 2:", ans)
    # ans = main2(lines_)
    # print("part 2:", ans)
