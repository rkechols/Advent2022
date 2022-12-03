fun priority(s: Char): Int {
    var base_score = 1 + s.lowercaseChar().code - 'a'.code
    if (s == s.uppercaseChar()) {
        base_score += 26
    }
    return base_score
}


fun solve1(lines: List<String>): Int {
    var total = 0
    for (line in lines) {
        val half = line.length / 2
        val left = line.substring(0, half)
        val right = line.substring(half)
        val overlap = (left.toSet().intersect(right.toSet())).first()
        total += priority(overlap)
    }
    return total
}


fun solve2(lines: List<String>): Int {
    val group_size = 3
    var total = 0
    for (i in 0 until lines.size step group_size) {
        var working_set = lines[i].toSet()
        for (j in i + 1 until i + group_size) {
            working_set = working_set.intersect(lines[j].toSet())
        }
        val overlap = working_set.first()
        total += priority(overlap)
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
