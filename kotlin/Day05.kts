val digit_regex = Regex("\\d+")
val instruction_regex = Regex("move (\\d+) from (\\d+) to (\\d+)")

fun parse(input: String): Pair<Map<Int, List<Char>>, List<Triple<Int, Int, Int>>> {
    val blocks = input.split("\n\n")
    // top chunk
    val start_config = blocks[0].split("\n")
    val cols = LinkedHashMap<Int, List<Char>>()
    for (match in digit_regex.findAll(start_config[start_config.size - 1])) {
        val col = match.value.toInt()
        val loc = match.range.start
        val this_col = mutableListOf<Char>()
        for (i in start_config.size - 2 downTo 0) {
            val line = start_config[i]
            val sym = try {
                line[loc]
            } catch (e: StringIndexOutOfBoundsException) {
                println("caught: $e")
                break
            }
            if (sym.isWhitespace()) {
                break
            }
            this_col.add(sym)
        }
        cols[col] = this_col
    }
    // bottom chunk
    val instructions_block = blocks[1].split("\n")
    val instructions = mutableListOf<Triple<Int, Int, Int>>()
    for (instruction in instructions_block) {
        val match = instruction_regex.matchEntire(instruction)!!
        val match_vals = match.groupValues.drop(1).map{ it.toInt() }
        instructions.add(Triple(match_vals[0], match_vals[1], match_vals[2]))
    }
    return Pair(cols, instructions)
}


fun copy_cols(cols_orig: Map<Int, List<Char>>): Map<Int, MutableList<Char>> {
    val cols = LinkedHashMap<Int, MutableList<Char>>()
    for ((key, value) in cols_orig.entries.iterator()) {
        val list_copy = mutableListOf<Char>()
        list_copy.addAll(value)
        cols[key] = list_copy
    }
    return cols
}


fun solve1(cols_orig: Map<Int, List<Char>>, instructions: List<Triple<Int, Int, Int>>): List<Char> {
    val cols = copy_cols(cols_orig)
    for ((count, start, end) in instructions) {
        for (i in 0 until count) {
            val sym = cols[start]!!.removeLast()
            cols[end]!!.add(sym)
        }
    }
    val chars = cols.values.map{ it[it.size - 1]}
    return chars
}


fun solve2(cols_orig: Map<Int, List<Char>>, instructions: List<Triple<Int, Int, Int>>): List<Char> {
    val cols = copy_cols(cols_orig)
    for ((count, start, end) in instructions) {
        val start_col = cols[start]!!
        val stack = start_col.slice(start_col.size - count until start_col.size)
        for (i in 0 until count) {
            start_col.removeLast()
        }
        cols[end]!!.addAll(stack)
    }
    val chars = cols.values.map{ it[it.size - 1]}
    return chars
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
    val (cols, instructions) = parse(input)
    val answer1 = solve1(cols, instructions).joinToString("")
    println("part 1: $answer1")
    val answer2 = solve2(cols, instructions).joinToString("")
    println("part 2: $answer2")
}

main()
