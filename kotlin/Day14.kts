typealias Loc = Pair<Int, Int>

val ROCK = '#'
val SAND = 'o'
val AIR = '.'

val START = Loc(500, 0)


class Cave {
    val data = mutableMapOf<Loc, Char>()

    fun loc_is_free(loc: Loc): Boolean {
        val value = data.getOrDefault(loc, AIR)
        return value != ROCK && value != SAND
    }

    operator fun get(key: Loc): Char {
        return data[key]!!
    }

    operator fun set(key: Loc, value: Char) {
        data[key] = value
    }

    fun draw() {
        val x_vals = data.keys.map{ it.first }
        val y_vals = data.keys.map{ it.second }
        val min_x = x_vals.min()
        val max_x = x_vals.max()
        val min_y = y_vals.min()
        val max_y = y_vals.max()
        val n_rows = 1 + max_y - min_y
        val n_cols = 1 + max_x - min_x
        val canvas = Array(n_rows){ Array(n_cols){ AIR } }
        for ((loc, value) in data.entries) {
            val (x, y) = loc
            canvas[y - min_y][x - min_x] = value
        }
        for (row in canvas) {
            for (c in row) {
                print(c)
            }
            println()
        }
    }

    fun lowest_rock(): Int {
        return data.entries.filter{ pair -> pair.value == ROCK }.map{ pair -> pair.key.second }.max()
    }
}


class Sand(loc_: Loc) {
    var x = loc_.first
        private set
    var y = loc_.second
        private set

    val loc: Loc
        get() = Loc(x, y)

    fun fall(cave: Cave, floor: Int? = null): Boolean {
        val next_y = y + 1
        if (next_y == floor) {
            return false
        }
        for (next_x in listOf(x, x - 1, x + 1)) {
            if (cave.loc_is_free(Loc(next_x, next_y))) {
                x = next_x
                y = next_y
                return true
            }
        }
        // can't go anywhere
        return false
    }
}


fun parse(lines: List<String>): Cave {
    val cave = Cave()
    for (line in lines) {
        var prev: Loc? = null
        for (point_str in line.split("->")) {
            val cur_list = point_str.trim().split(",").map{ it.toInt() }
            val cur = Loc(cur_list[0], cur_list[1])
            if (prev != null) {
                if (prev.first == cur.first) {
                    val (low, high) = if (prev.second <= cur.second) {
                        Pair(prev.second, cur.second)
                    } else {
                        Pair(cur.second, prev.second)
                    }
                    for (y in low..high) {
                        cave[Loc(prev.first, y)] = ROCK
                    }
                } else if (prev.second == cur.second) {
                    val (low, high) = if (prev.first <= cur.first) {
                        Pair(prev.first, cur.first)
                    } else {
                        Pair(cur.first, prev.first)
                    }
                    for (x in low..high) {
                        cave[Loc(x, prev.second)] = ROCK
                    }
                } else {
                    error("cannot draw line from $prev to $cur")
                }
            }
            prev = cur
        }
    }
    return cave
}


fun solve(cave: Cave, floor_terminates: Boolean): Int {
    var count = 0
    val lowest = cave.lowest_rock()
    val floor = lowest + 2
    while (cave.loc_is_free(START)) {
        val cur = Sand(START)
        while (cur.fall(cave, floor)) {
            if (floor_terminates && cur.y > lowest) {
                // it went below lowest rock; next move would hit the floor
                return count
            }
        }
        cave[cur.loc] = SAND
        count++
    }
    return count
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
    val cave1 = parse(lines)
    cave1.draw()
    val answer1 = solve(cave1, floor_terminates = true)
    println("part 1: $answer1")
    val cave2 = parse(lines)
    val answer2 = solve(cave2, floor_terminates = false)
    println("part 2: $answer2")
}

main()
