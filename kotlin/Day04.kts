fun priority(s: Char): Int {
    var base_score = 1 + s.lowercaseChar().code - 'a'.code
    if (s == s.uppercaseChar()) {
        base_score += 26
    }
    return base_score
}


fun solve1(lines: List<String>): Int {
    var count = 0
    for (line in lines) {
        val parts = line.split(",")
        val first_split = parts[0].split("-")
        val first_start = first_split[0].toInt()
        val first_end = first_split[1].toInt()
        val second_split = parts[1].split("-")
        val second_start = second_split[0].toInt()
        val second_end = second_split[1].toInt()
        if (first_start <= second_start && first_end >= second_end || second_start <= first_start && second_end >= first_end) {
            count += 1
        }
    }
    return count
}


fun solve2(lines: List<String>): Int {
    var count = 0
    for (line in lines) {
        val parts = line.split(",")
        val first_split = parts[0].split("-")
        val first_start = first_split[0].toInt()
        val first_end = first_split[1].toInt()
        val second_split = parts[1].split("-")
        val second_start = second_split[0].toInt()
        val second_end = second_split[1].toInt()
        if ((first_start..first_end).toSet().intersect((second_start..second_end).toSet()).size > 0) {
            count += 1
        }
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
    val answer1 = solve1(lines)
    println("part 1: $answer1")
    val answer2 = solve2(lines)
    println("part 2: $answer2")
}

main()
