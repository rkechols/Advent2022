import copy
import heapq
import random
import re
from pathlib import Path
from typing import List, Dict, Set, Tuple, Optional

from constants import INPUTS_DIR, UTF_8

INPUT_PATH = Path(INPUTS_DIR) / "day-16.txt"
# INPUT_PATH = Path(INPUTS_DIR) / "example.txt"

LINE_RE = re.compile(r"Valve (.*) has flow rate=(\d+); tunnels? leads? to valves? (.*)")

START = "AA"
TIME_LIMIT = 30

random.seed(4)


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


def greedy(flows: Dict[str, int], adj: Dict[str, Set[str]]) -> int:
    timer = TIME_LIMIT
    opened = {START: 0}
    cur = START
    while timer > 0:
        timer -= 1
        if cur not in opened and flows[cur] > 0:
            opened[cur] = timer
        else:
            cur = random.choice(sorted(adj[cur]))
    return sum(
        flows[valve] * steps_open
        for valve, steps_open in opened.items()
    )


class PartialSolution:
    __slots__ = "cur", "timer", "flows", "adj", "opened", "unopened", "_score"

    def __init__(self, *, cur: str, timer: int,
                 flows: Dict[str, int], adj: Dict[str, Set[str]],
                 opened: Dict[str, int], unopened: Set[str]):
        self.cur = cur
        self.timer = timer
        self.flows = flows
        self.adj = adj
        self.opened = opened
        self.unopened = unopened
        # late init:
        self._score: Optional[int] = None

    def score(self) -> int:
        return sum(
            self.flows[valve] * steps_open
            for valve, steps_open in self.opened.items()
        )

    def score_hypothetical(self) -> int:
        if self._score is None:
            so_far = self.score()
            sorted_remaining_flows = sorted(
                flow
                for valve in self.unopened
                if (flow := self.flows[valve]) > 0
            )
            shift = -1 if self.can_open() else 0
            hypothetical = sum(
                flow * steps_remaining
                for flow, steps_remaining in zip(
                    reversed(sorted_remaining_flows),
                    range(self.timer + shift, 0, -2)
                )
            )
            self._score = so_far + hypothetical
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
            cur=self.cur,
            timer=self.timer,
            flows=self.flows,
            adj=self.adj,
            opened=copy.copy(self.opened),
            unopened=copy.copy(self.unopened),
        )

    def children(self) -> List['PartialSolution']:
        to_return = []
        # open this valve
        if self.can_open():
            child = self.clone()
            child.open()
            to_return.append(child)
        # go to each neighbor
        for neighbor in self.adj[self.cur]:
            child = self.clone()
            child.move(neighbor)
            to_return.append(child)
        return to_return

    def can_open(self) -> bool:
        return (self.cur not in self.opened) and (self.flows[self.cur] > 0)

    def open(self):
        if not self.can_open():
            raise ValueError(f"try to open {self.cur}, which is already open")
        self.timer -= 1
        self.opened[self.cur] = self.timer
        self.unopened.remove(self.cur)
        self._score = None

    def move(self, dest: str):
        self.timer -= 1
        self.cur = dest
        # self._score = None


class HeapElem:
    __slots__ = "val", "score"

    def __init__(self, val: PartialSolution):
        self.val = val
        self.score = val.score_heap()

    def __lt__(self, other: 'HeapElem') -> bool:
        return self.score < other.score

    # def __gt__(self, other: 'HeapElem') -> bool:
    #     return self.score > other.score
    #
    # def __eq__(self, other: 'HeapElem') -> bool:
    #     return self.score == other.score


def main(flows: Dict[str, int], adj: Dict[str, Set[str]]) -> int:
    best_score = greedy(flows, adj)
    print("greedy score:", best_score)
    heap = [HeapElem(PartialSolution(
        cur=START,
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
        for possible_child in state.children():
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
    print("part 1:", ans)
