val ORDER_THEM = listOf('A', 'B', 'C')
val ORDER_ME = listOf('X', 'Y', 'Z')


fun solve1(lines: List<String>): Int {
    var total = 0
    for (line in lines) {
        val them = line[0]
        val me = line[2]
        val them_index = ORDER_THEM.indexOf(them)
        val me_index = ORDER_ME.indexOf(me)
        total += me_index + 1  // for item
        total += (1 + me_index - them_index).mod(3) * 3  // for win
    }
    return total
}


fun solve2(lines: List<String>): Int {
    var total = 0
    for (line in lines) {
        val them = line[0]
        val me = line[2]
        val them_index = ORDER_THEM.indexOf(them)
        val me_index = ORDER_ME.indexOf(me)
        total += 1 + (them_index + me_index - 1).mod(3)  // for item
        total += me_index * 3  // for win
    }
    return total
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
    val answer1 = solve1(lines)
    println("part 1: $answer1")
    val answer2 = solve2(lines)
    println("part 2: $answer2")
}

main()
