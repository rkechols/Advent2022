import kotlin.math.abs
import kotlin.math.sign


class Knot(public var x: Int = 0, public var y: Int = 0) {
    companion object {
        val DIRECTIONS = mapOf(
            "R" to Pair(1, 0),
            "L" to Pair(-1, 0),
            "U" to Pair(0, 1),
            "D" to Pair(0, -1),
        )
    }

    fun shift(dir_tuple: Pair<Int, Int>) {
        x += dir_tuple.first
        y += dir_tuple.second
    }

    fun follow(head: Knot) {
        if (head.x == x) {
            if (head.y > y + 1) {
                y++
            } else if (head.y < y - 1) {
                y--
            }
        } else if (head.y == y) {
            if (head.x > x + 1) {
                x++
            } else if (head.x < x - 1) {
                x--
            }
        } else {  // diagonal
            val x_diff = head.x - x
            val y_diff = head.y - y
            if (abs(x_diff) > 1 || abs(y_diff) > 1) {
                shift(Pair(x_diff.sign, y_diff.sign))
            }
        }
    }

    fun to_tuple() = Pair(x, y)
}


fun solve(steps: List<Pair<String, Int>>, n_knots: Int = 2): Int {
    val knots = Array(n_knots){ Knot() }
    val tail_visited = mutableSetOf(knots.last().to_tuple())
    for ((direction, step_count) in steps) {
        val head_shift = Knot.DIRECTIONS[direction]!!
        for (i_step in 0 until step_count) {
            knots.first().shift(head_shift)
            for (i in 1 until n_knots) {
                knots[i].follow(knots[i - 1])
            }
            tail_visited.add(knots.last().to_tuple())
        }
    }
    return tail_visited.size
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
    val steps = mutableListOf<Pair<String, Int>>()
    for (line in lines) {
        val line_split = line.split(" ")
        steps.add(Pair(line_split[0], line_split[1].toInt()))
    }
    val answer1 = solve(steps, n_knots=2)
    println("part 1: $answer1")
    val answer2 = solve(steps, n_knots=10)
    println("part 2: $answer2")
}

main()
