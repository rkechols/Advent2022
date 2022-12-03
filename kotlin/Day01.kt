fun solve(lines: List<String>, top_k: Int = 1): Int {
    val elf_counts = mutableListOf<Int>()
    var this_elf = 0
    for (line in lines) {
        if (line == "") {
            elf_counts.add(this_elf)
            this_elf = 0
        } else {
            this_elf += line.toInt()
        }
    }
    elf_counts.add(this_elf)
    // get top k
    val tops = mutableListOf<Int>()
    for (count in elf_counts) {
        tops.add(count)
        tops.sortDescending()
        if (tops.size > top_k) {
            tops.removeLast()
        }
    }
    return tops.sum()
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
    val answer1 = solve(lines, top_k=1)
    println("part 1: $answer1")
    val answer2 = solve(lines, top_k=3)
    println("part 2: $answer2")
}
