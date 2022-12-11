import java.util.LinkedList
import java.util.Queue

val MONKEY_RE = Regex("Monkey (\\d+):")
val OPERATION_RE = Regex("new = old ([+*]) (.+)")
val DIVISION_RE = Regex("Test: divisible by (\\d+)")
val TRUE_RE = Regex("If true: throw to monkey (\\d+)")
val False_RE = Regex("If false: throw to monkey (\\d+)")


fun parse_operation(operation_spec: Pair<String, String>): (Long) -> Long {
    val (op, num) = operation_spec
    return if (op == "+") {
        if (num == "old") {
            { it + it }
        } else {
            { it + num.toInt() }
        }
    } else if (op == "*") {
        if (num == "old") {
            { it * it }
        } else {
            { it * num.toInt() }
        }
    } else {
        throw Error("Bad operator: $op")
    }
}


class Monkey(
        items_: List<Long>,
        operation_spec: Pair<String, String>,
        public val divisor: Int,
        private val true_dest: Int,
        private val false_dest: Int,
) {
    private val items: Queue<Long> = LinkedList<Long>(items_)
    private val operation = parse_operation(operation_spec)

    public val n_items: Int
        get() = items.size

    fun pop_item(): Long = items.remove()

    fun catch_item(item: Long) {
        items.add(item)
    }

    fun do_operation(item: Long): Long {
        return operation(item)
    }

    fun get_dest(item: Long): Int {
        return if (item.mod(divisor) == 0) {
            true_dest
        } else {
            false_dest
        }
    }
}


fun parse(data: String): List<Monkey> {
    val monkey_blocks = data.split("\n\n")
    val to_return = mutableListOf<Monkey>()
    var next_i = 0
    for (monkey_block in monkey_blocks) {
        val monkey_lines = monkey_block.split("\n")
        val num = MONKEY_RE.matchEntire(monkey_lines[0].trim())!!.groupValues[1].toInt()
        if (num != next_i) {
            throw Error("wrong order of monkeys! expected $next_i but got $num")
        }
        next_i++
        val starting_items = monkey_lines[1].split(":")[1].trim().split(", ").map{ it.toLong() }
        val operation_spec_ = OPERATION_RE.matchEntire(monkey_lines[2].split(":")[1].trim())!!.groupValues.drop(1)
        val operation_spec = Pair(operation_spec_[0], operation_spec_[1])
        val divisor = DIVISION_RE.matchEntire(monkey_lines[3].trim())!!.groupValues[1].toInt()
        val true_dest = TRUE_RE.matchEntire(monkey_lines[4].trim())!!.groupValues[1].toInt()
        val false_dest = False_RE.matchEntire(monkey_lines[5].trim())!!.groupValues[1].toInt()
        val monkey = Monkey(
                starting_items,
                operation_spec,
                divisor,
                true_dest,
                false_dest,
        )
        to_return.add(monkey)
    }
    return to_return
}


fun solve(monkeys: List<Monkey>, n_rounds: Int = 20, reduction: (Long) -> Long): Long {
    val inspect_counts = Array<Long>(monkeys.size){ 0 }
    repeat(n_rounds) {
        for ((i, monkey) in monkeys.withIndex()) {
            while (monkey.n_items > 0) {
                var item = monkey.pop_item()
                item = monkey.do_operation(item)
                inspect_counts[i]++
                item = reduction(item)
                val dest = monkey.get_dest(item)
                monkeys[dest].catch_item(item)
            }
        }
    }
    inspect_counts.sort()
    val a = inspect_counts[inspect_counts.size - 2]
    val b = inspect_counts[inspect_counts.size - 1]
    return a * b
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
    val raw = lines.joinToString("\n")
    val monkeys1 = parse(raw)
    val answer1 = solve(monkeys1, n_rounds = 20, reduction = { it: Long -> it / 3 })
    println("part 1: $answer1")
    val monkeys2 = parse(raw)
    val mod_n = monkeys2.map{ it.divisor }.reduce{ acc, it -> acc * it }.toLong()
    val answer2 = solve(monkeys2, n_rounds = 10000, reduction = { it: Long -> it.mod(mod_n) })
    println("part 2: $answer2")
}

main()
