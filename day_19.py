import copy
import re
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Set, Tuple

from tqdm import tqdm

from constants import INPUTS_DIR, UTF_8

INPUT_PATH = Path(INPUTS_DIR) / "day-19.txt"
# INPUT_PATH = Path(INPUTS_DIR) / "example.txt"

INT_RE = re.compile(r"\d+")

N_MINUTES = 24


@dataclass(frozen=True)
class Blueprint:
    label: int
    ore_bot_ore: int
    clay_bot_ore: int
    obs_bot_ore: int
    obs_bot_clay: int
    geo_bot_ore: int
    geo_bot_obs: int


def parse(lines: List[str]) -> List[Blueprint]:
    to_return = []
    for line in lines:
        bp_label, remaining = line.split(":")
        bp_label = int(bp_label.split()[1])
        ore_bot, clay_bot, obs_bot, geo_bot = remaining[:-1].split(".")
        ore_bot_ore = int(INT_RE.search(ore_bot).group(0))
        clay_bot_ore = int(INT_RE.search(clay_bot).group(0))
        obs_bot_ore, obs_bot_clay = map(int, INT_RE.findall(obs_bot))
        geo_bot_ore, geo_bot_obs = map(int, INT_RE.findall(geo_bot))
        to_return.append(Blueprint(
            label=bp_label,
            ore_bot_ore=ore_bot_ore,
            clay_bot_ore=clay_bot_ore,
            obs_bot_ore=obs_bot_ore,
            obs_bot_clay=obs_bot_clay,
            geo_bot_ore=geo_bot_ore,
            geo_bot_obs=geo_bot_obs,
        ))
    return to_return


class Mine:
    __slots__ = "blueprint", "n_ore_bots", "n_clay_bots", "n_obs_bots", "n_geo_bots", "n_ore", "n_clay", "n_obs", "n_geo"

    def __init__(self, blueprint: Blueprint):
        self.blueprint = blueprint
        # bots
        self.n_ore_bots = 1
        self.n_clay_bots = 0
        self.n_obs_bots = 0
        self.n_geo_bots = 0
        # minerals
        self.n_ore = 0
        self.n_clay = 0
        self.n_obs = 0
        self.n_geo = 0

    def to_tuple(self) -> Tuple[int, int, int, int]:
        return self.n_ore_bots, self.n_clay_bots, self.n_obs_bots, self.n_geo_bots

    def collect(self):
        self.n_ore += self.n_ore_bots
        self.n_clay += self.n_clay_bots
        self.n_obs += self.n_obs_bots
        self.n_geo += self.n_geo_bots

    def build_options(self) -> Set[Optional[str]]:
        # check if we can build each type of bot
        options = {None}
        if self.n_ore >= self.blueprint.geo_bot_ore and self.n_obs >= self.blueprint.geo_bot_obs:
            return {"geo"}  # force geo if we can do it
        if self.n_ore >= self.blueprint.obs_bot_ore and self.n_clay >= self.blueprint.obs_bot_clay \
                and self.n_obs_bots < self.blueprint.geo_bot_obs:
            options.add("obs")
        if self.n_ore >= self.blueprint.clay_bot_ore \
                and self.n_clay_bots < self.blueprint.obs_bot_clay:
            options.add("clay")
        if self.n_ore >= self.blueprint.ore_bot_ore and self.n_ore_bots < max(
                self.blueprint.ore_bot_ore,
                self.blueprint.clay_bot_ore,
                self.blueprint.obs_bot_ore,
                self.blueprint.geo_bot_ore,
        ):
            options.add("ore")
        return options

    def build_spend(self, bot_type: Optional[str]):
        match bot_type:
            case "geo":
                self.n_ore -= self.blueprint.geo_bot_ore
                self.n_obs -= self.blueprint.geo_bot_obs
            case "obs":
                self.n_ore -= self.blueprint.obs_bot_ore
                self.n_clay -= self.blueprint.obs_bot_clay
            case "clay":
                self.n_ore -= self.blueprint.clay_bot_ore
            case "ore":
                self.n_ore -= self.blueprint.ore_bot_ore
            case None:
                pass
            case _:
                raise ValueError(f"unexpected bot_type: {bot_type}")

    def build_finish(self, bot_type: Optional[str]):
        match bot_type:
            case "geo":
                self.n_geo_bots += 1
            case "obs":
                self.n_obs_bots += 1
            case "clay":
                self.n_clay_bots += 1
            case "ore":
                self.n_ore_bots += 1
            case None:
                pass
            case _:
                raise ValueError(f"unexpected bot_type: {bot_type}")


def get_max_geodes(blueprint: Blueprint) -> int:
    start_state = Mine(blueprint)
    mines = [start_state]
    states_seen = {start_state.to_tuple()}
    for cur_minute in range(1, N_MINUTES + 1):
        mines_new = []
        states_seen_new = set()
        for mine in mines:
            options = mine.build_options()
            for to_build in options:
                mine_option = copy.copy(mine)
                mine_option.build_spend(to_build)
                mine_option.collect()
                mine_option.build_finish(to_build)
                mine_tup = mine_option.to_tuple()
                # skip ones where we build a new bot when we could've done so earlier
                if to_build is None or mine_tup not in states_seen:
                    mines_new.append(mine_option)
                    states_seen_new.add(mine_tup)
        if len(mines_new) == 0:
            raise RuntimeError("ALGORITHM ERROR: no options")
        mines = mines_new
        states_seen.update(states_seen_new)
    return max(mine.n_geo for mine in mines)


def main(blueprints: List[Blueprint]) -> int:
    total = 0
    for blueprint in tqdm(blueprints):
        max_geodes = get_max_geodes(blueprint)
        total += max_geodes * blueprint.label
    return total


if __name__ == "__main__":
    with open(INPUT_PATH, "r", encoding=UTF_8) as f:
        lines_ = [line_.strip() for line_ in f.readlines()]
    blueprints_ = parse(lines_)
    ans = main(blueprints_)
    print("part 1:", ans)
    # ans = main2(lines_)
    # print("part 2:", ans)
