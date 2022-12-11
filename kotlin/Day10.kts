import kotlin.math.abs


val N_ROWS = 6
val N_COLS = 40


fun check_cycle(cycle: Int) = (cycle - 20).mod(40) == 0


fun cycle_to_row_col(cycle_: Int): Pair<Int, Int> {
    val cycle = cycle_ - 1
    val row = (cycle / N_COLS).mod(N_ROWS)
    val col = cycle.mod(N_COLS)
    return Pair(row, col)
}


fun try_draw(screen: Array<Array<Char>>, x: Int, cycle: Int) {
    val (row, col) = cycle_to_row_col(cycle)
    if (abs(x - col) <= 1) {
        screen[row][col] = '#'
    }
}


fun solve(lines: List<String>): Pair<Int, Array<Array<Char>>> {
    var cycle = 0
    var x = 1
    var total_strength = 0
    val screen = Array(N_ROWS){ Array(N_COLS){ '.' } }
    for (line in lines) {
        if (line == "noop") {
            cycle++
            try_draw(screen, x, cycle)
            if (check_cycle(cycle)) {
                total_strength += cycle * x
            }
        } else if (line.startsWith("addx")) {
            repeat(2) {
                cycle++
                try_draw(screen, x, cycle)
                if (check_cycle(cycle)) {
                    total_strength += cycle * x
                }
            }
            x += line.slice(5 until line.length).toInt()
        } else {
            throw Error("bad line: $line")
        }
    }
    return Pair(total_strength, screen)
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
    val (ans, drawing) = solve(lines)
    println("part 1: $ans")
    println("part 2:")
    for (row in drawing) {
        println(row.joinToString(""))
    }
}

main()
