val THRESHOLD = 100000

val CD_RE = Regex("\\$ cd (.+)")
val FILE_RE = Regex("(\\d+) (.+)")

val TOTAL = 70000000
val TOTAL_NEEDED = 30000000


class Dir(val name: String) {
    val files = mutableMapOf<String, Int>()
    val dirs = mutableMapOf<String, Dir>()
    private var _size: Int? = null
    public val size: Int
        get() {
            val size_copy = _size
            return if (size_copy == null) {
                calc_size()
            } else {
                size_copy
            }
        }

    fun add_dir(name: String) {
        _size = null
        dirs[name] = Dir(name)
    }

    fun add_file(file: Pair<Int, String>) {
        _size = null
        val (file_size, file_name) = file
        files[file_name] = file_size
    }

    fun calc_size(): Int {
        var calc = files.values.sum()
        for (subdir in dirs.values) {
            calc += subdir.calc_size()
        }
        _size = calc
        return calc
    }
}


fun try_cd(s: String): String? {
    val match = CD_RE.matchEntire(s)
    return if (match == null) {
        null
    } else {
        match.groupValues[1]
    }
}


fun try_ls(s: String): Boolean {
    return s == "$ ls"
}


fun try_dir(s: String): String? {
    return if (s.startsWith("dir ")) {
        s.drop(4)
    } else { null }
}

fun try_file(s: String): Pair<Int, String>? {
    val match = FILE_RE.matchEntire(s)
    return if (match == null) {
        null
    } else {
        Pair(match.groupValues[1].toInt(), match.groupValues[2])
    }
}


fun get_cur_dir(root: Dir, path: List<String>): Dir {
    var cur = root
    for (dir_name in path) {
        cur = cur.dirs[dir_name]!!
    }
    return cur
}


fun select_dirs(cur: Dir, selector: (d: Dir) -> Boolean, results_: MutableList<Dir>? = null): List<Dir> {
    val results = results_ ?: mutableListOf()
    if (selector(cur)) {
        results.add(cur)
    }
    for (subdir in cur.dirs.values) {
        select_dirs(subdir, selector, results)
    }
    return results
}


fun solve1(lines: List<String>): Pair<Int, Dir> {
    val root = Dir("/")
    val path = mutableListOf<String>()
    var i = 0
    while (i < lines.size) {
        val line = lines[i]
        val result_cd = try_cd(line)
        if (result_cd != null) {
            if (result_cd == "..") {
                path.removeLast()
            } else if (result_cd == "/") {
                path.clear()
            } else {
                path.add(result_cd)
            }
        } else if (try_ls(line)) {
            i++
            val cur_dir = get_cur_dir(root, path)
            while (i < lines.size) {
                val result_dir = try_dir(lines[i])
                if (result_dir != null) {
                    cur_dir.add_dir(result_dir)
                } else {
                    val result_file = try_file(lines[i])
                    if (result_file != null) {
                        cur_dir.add_file(result_file)
                    } else {
                        i--  // so the next +1 goes to the line we just tried
                        break
                    }
                }
                i++
            }
        } else {
            throw Error("unknown command, line $i: $line")
        }
        i++
    }
    // recursively find sizes
    root.calc_size()
    // find small dirs
    val small_dirs = select_dirs(root, { it.size <= THRESHOLD })
    return Pair(
        small_dirs.sumOf{ it.size },
        root,
    )
}


fun solve2(root: Dir): Int {
    val unused = TOTAL - root.size
    val additional_needed = TOTAL_NEEDED - unused
    if (additional_needed <= 0) {
        return 0
    }
    val dirs_big_enough = select_dirs(root, { it.size >= additional_needed})
    return dirs_big_enough.minOf{ it.size }
}


fun main() {
    val lines = mutableListOf<String>()
    while (true) {
        val line = readLine()
        if (line == null) {
            break
        }
        lines.add(line)
    }
    val (answer1, root) = solve1(lines)
    println("part 1: $answer1")
    val answer2 = solve2(root)
    println("part 2: $answer2")
}
