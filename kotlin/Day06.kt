fun solve(s: String, k: Int): Int {
    for (i in 0 until (s.length - k)) {
        if (s.slice(i until i + k).toSet().size == k) {
            return i + k
        }
    }
    throw Error("no answer found")
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
    val input = lines.joinToString("\n")
    val answer1 = solve(input, 4)
    println("part 1: $answer1")
    val answer2 = solve(input, 14)
    println("part 2: $answer2")
}
