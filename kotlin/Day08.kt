fun solve1(forest: List<List<Int>>): Int {
    val n_rows = forest.size
    val n_cols = forest[0].size
    val visible = Array(n_rows){ Array(n_cols){ false } }
    for (i in 0 until n_rows) {
        visible[i][0] = true
        visible[i][n_cols - 1] = true
    }
    for (i in 0 until n_cols) {
        visible[0][i] = true
        visible[n_rows - 1][i] = true
    }
    // analyze from 4 sides
    for (row in 0 until n_rows) {
        // from left
        var tallest = forest[row][0]
        for (col in 1 until n_cols) {
            if (forest[row][col] > tallest) {
                tallest = forest[row][col]
                visible[row][col] = true
            }
        }
        // from right
        tallest = forest[row][n_cols - 1]
        for (col in (n_cols - 2) downTo 0) {
            if (forest[row][col] > tallest) {
                tallest = forest[row][col]
                visible[row][col] = true
            }
        }
    }
    for (col in 0 until n_cols) {
        // from up
        var tallest = forest[0][col]
        for (row in 1 until n_rows) {
            if (forest[row][col] > tallest) {
                tallest = forest[row][col]
                visible[row][col] = true
            }
        }
        // from down
        tallest = forest[n_rows - 1][col]
        for (row in (n_rows - 2) downTo 0) {
            if (forest[row][col] > tallest) {
                tallest = forest[row][col]
                visible[row][col] = true
            }
        }
    }
    return visible.sumOf{ it.count{ it } }
}


fun score(forest: List<List<Int>>, row: Int, col: Int): Int {
    val n_rows = forest.size
    val n_cols = forest[0].size
    val this_height = forest[row][col]
    // up
    var up_: Int? = null
    for (i in (row - 1) downTo 0) {
        if (forest[i][col] >= this_height) {
            up_ = row - i
            break
        }
    }
    val up = up_ ?: row
    // down
    var down_: Int? = null
    for (i in (row + 1) until n_rows) {
        if (forest[i][col] >= this_height) {
            down_ = i - row
            break
        }
    }
    val down = down_ ?: (n_rows - row - 1)
    // left
    var left_: Int? = null
    for (i in (col - 1) downTo 0) {
        if (forest[row][i] >= this_height) {
            left_ = col - i
            break
        }
    }
    val left = left_ ?: col
    // right
    var right_: Int? = null
    for (i in (col + 1) until n_cols) {
        if (forest[row][i] >= this_height) {
            right_ = i - col
            break
        }
    }
    val right = right_ ?: (n_cols - col - 1)
    return up * down * left * right
}


fun solve2(forest: List<List<Int>>): Int {
    var highest = 0
    for (i in 1 until (forest.size - 1)) {
        for (j in 1 until (forest[0].size - 1)) {
            val this_score = score(forest, i, j)
            if (this_score > highest) {
                highest = this_score
            }
        }
    }
    return highest
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
    val forest = lines.map{ it.map{ it.digitToInt() } }
    val answer1 = solve1(forest)
    println("part 1: $answer1")
    val answer2 = solve2(forest)
    println("part 2: $answer2")
}
