import re
from pathlib import Path
from typing import List, Optional, Tuple, Dict

from constants import INPUTS_DIR, UTF_8

INPUT_PATH = Path(INPUTS_DIR) / "day-07.txt"
# INPUT_PATH = Path(INPUTS_DIR) / "example.txt"


THRESHOLD = 100000
CD_RE = re.compile(r"\$ cd (.+)")
FILE_RE = re.compile(r"(\d+) (.*)")


TOTAL = 70000000
NEED = 30000000


class Dir:
    def __init__(self, name: str):
        self.name = name
        self.files: List[Tuple[int, str]] = []
        self.dirs: Dict[str, 'Dir'] = {}
        self._size: Optional[int] = None

    def add_dir(self, name: str):
        self.dirs[name] = Dir(name)
        self._size = None

    def add_file(self, file: Tuple[int, str]):
        self.files.append(file)
        self._size = None

    def calc_size(self) -> int:
        size = sum(file[0] for file in self.files)
        for subdir in self.dirs.values():
            size += subdir.calc_size()
        self._size = size
        return self._size

    @property
    def size(self) -> Optional[int]:
        return self._size


def try_cd(s: str) -> Optional[str]:
    if (match := CD_RE.fullmatch(s)) is not None:
        return match.group(1)
    return None


def try_ls(s: str) -> bool:
    return s == "$ ls"


def try_dir(s: str) -> Optional[str]:
    if s.startswith("dir "):
        return s[4:]
    return None


def try_file(s: str) -> Optional[Tuple[int, str]]:
    if (match := FILE_RE.fullmatch(s)) is not None:
        size, name = match.groups()
        return int(size), name
    return None


def get_cur_dir(root: Dir, path: List[str]) -> Dir:
    cur = root
    for dir_name in path:
        cur = cur.dirs[dir_name]
    return cur


def get_small_dirs(cur: Dir, results: List[Dir]):
    if cur.size <= THRESHOLD:
        results.append(cur)
    for subdir in cur.dirs.values():
        get_small_dirs(subdir, results)


def main1(lines: List[str]) -> Tuple[int, Dir]:
    root = Dir("/")
    path = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if (result := try_cd(line)) is not None:
            if result == "..":
                path.pop()
            elif result == "/":
                path.clear()
            else:
                path.append(result)
        elif try_ls(line):
            i += 1
            cur_dir = get_cur_dir(root, path)
            while i < len(lines):
                if (result := try_dir(lines[i])) is not None:
                    cur_dir.add_dir(result)
                elif (result := try_file(lines[i])) is not None:
                    cur_dir.files.append(result)
                else:
                    i -= 1  # so the next +1 goes to the line we just tried
                    break
                i += 1
        else:
            raise ValueError(f"unknown command, line {i}: {line}")
        i += 1
    # recursively find sizes
    root.calc_size()
    # find small dirs
    results = []
    get_small_dirs(root, results)
    return sum(d.size for d in results), root


def get_big_dirs(cur: Dir, results: List[Dir], threshold: int):
    if cur.size >= threshold:
        results.append(cur)
    for subdir in cur.dirs.values():
        get_big_dirs(subdir, results, threshold)


def main2(root: Dir) -> int:
    unused = TOTAL - root.size
    to_delete = NEED - unused
    if to_delete <= 0:
        return 0
    can_delete = []
    get_big_dirs(root, can_delete, to_delete)
    return min(d.size for d in can_delete)


if __name__ == "__main__":
    with open(INPUT_PATH, "r", encoding=UTF_8) as f:
        lines_ = [line_.strip() for line_ in f.readlines()]
    ans, root_ = main1(lines_)
    print("part 1:", ans)
    ans = main2(root_)
    print("part 2:", ans)
