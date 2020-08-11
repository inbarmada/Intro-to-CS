############################################################
# FILE : nonogram.py
# WRITER : Inbar Leibovich , inbarlei , 21395389
# EXERCISE : intro2cse Ex8 2020
# DESCRIPTION: 
# STUDENTS I DISCUSSED THE EXERCISE WITH: 
# WEB PAGES I USED: 
# NOTES:
############################################################


def get_row_variations(row, blocks):
    block_sums = []
    num_blocks = len(blocks)
    for ind in range(num_blocks):
        if ind == 0:
            block_sums.insert(0, blocks[num_blocks - ind - 1])
        else:
            block_sums.insert(0, blocks[num_blocks - ind - 1] + 1)
            block_sums[0] += block_sums[1]

    block_sums.append(0)
    li = []
    get_combos(row, block_sums, row[:], 0, 0, li)
    return li


def set_to_zeros(row, result, index, li):
    for i in range(index, len(row)):
        if row[i] == 1:
            return []
        else:
            result[i] = 0
    li.append(result)
    return result


def get_combos(row, block_sums, result, index, block_index, li):
    # If finished constraints, set rest of row to 0s
    if block_index == len(block_sums) - 1:
        set_to_zeros(row, result, index, li)

    elif index + block_sums[block_index] > len(row):
        return []

    else:
        combos = []
        if row[index] != 0:
            res = put_down_ones(row, block_sums, result[:], index, block_index, li)
            if res:
                combos.append(res)
        if row[index] != 1:
            res = put_down_a_zero(row, block_sums, result[:], index, block_index, li)
            if res:
                combos.append(res)
        return combos


def put_down_ones(row, block_sums, result, index, block_index, li):
    n = block_sums[block_index] - block_sums[block_index + 1]
    if block_sums[block_index + 1] != 0:
        n -= 1

        # If after n blocks is a 1, try moving up one
        if row[index + n + 1] == 1:
            return []
        else:
            result[index + n + 1] = 0

    broken = False
    for i in range(n):
        if row[index + i] != 0:
            result[index + i] = 1
        else:
            broken = True
            break

    if broken:
        return []
    else:
        if block_sums[block_index + 1] != 0:
            result[index + n] = 0
            n += 1

        return get_combos(row, block_sums, result, index + n, block_index + 1, li)


def put_down_a_zero(row, block_sums, result, index, block_index, li):
    result[index] = 0
    return get_combos(row, block_sums, result, index + 1, block_index, li)


# Must write a note at top of page
def get_intersection_row(rows):
    intersection = []
    for index in range(len(rows[0])):
        color = -1
        broken = False
        for row in rows:
            if color == -1:
                color = row[index]
            if row[index] == -1 or row[index] != color:
                broken = True
                break
        if not broken:
            intersection.append(color)
        else:
            intersection.append(-1)
    return intersection


# Only check rows/cols that contain -1s
def solve_easy_nonogram(constraints):
    num_rows = len(constraints[0])
    num_cols = len(constraints[1])
    board = [[-1]*num_cols] * num_rows
    prev_board = []
    while board != prev_board:
        print('boarddddd', board, prev_board)
        prev_board = deep_copy(board)

        # Evaluate for rows
        for row_ind in range(num_rows):
            consts = constraints[0][row_ind]
            possibilities = get_row_variations(board[row_ind], consts)
            if possibilities:
                board[row_ind] = get_intersection_row(possibilities)

        # Evaluate for columns
        for col_ind in range(num_cols):
            get_col = []
            for row_ind in range(len(board)):
                get_col.append(board[row_ind][col_ind])
            consts = constraints[1][col_ind]
            possibilities = get_row_variations(get_col, consts)
            if possibilities:
                col_res = get_intersection_row(possibilities)
                for row_ind in range(len(board)):
                    board[row_ind][col_ind] = col_res[row_ind]
    print('boarddddd', board)


def deep_copy(mat):
    res = []
    for i in range(len(mat)):
        row = []
        for j in range(len(mat[i])):
            row.append(mat[i][j])
        res.append(row)
    return res


def count_row_variations(length, blocks):
    # Empty row
    if len(blocks) == 0:
        return 1

    # Count black squares
    black = 0
    for i in blocks:
        black += i
    # Calculate number of spaces
    spaces = length - black

    # Calculate variations
    num = factorial(spaces - len(blocks) + 1, spaces + 1)
    num /= factorial(1, len(blocks))

    return num


def factorial(lower, n):
    fac = n
    for i in range(lower + 1, n):
        fac *= i
    return fac


def check_get_combos():
    my_row = [1, 1, -1, 0]
    my_constraints = [3]
    actual = get_row_variations(my_row, my_constraints)
    expected = [[1, 1, 1, 0]]
    assert sorted(actual) == sorted(expected), 'ac: ' + str(actual) + ' ex: ' + str(expected)

    my_row = [-1, -1, -1, 0]
    my_constraints = [2]
    actual = get_row_variations(my_row, my_constraints)
    expected = [[0, 1, 1, 0], [1, 1, 0, 0]]
    assert sorted(actual) == sorted(expected), 'ac: ' + str(actual) + ' ex: ' + str(expected)

    my_row = [-1, 0, 1, 0, -1, 0]
    my_constraints = [1, 1]
    actual = get_row_variations(my_row, my_constraints)
    expected = [[0, 0, 1, 0, 1, 0], [1, 0, 1, 0, 0, 0]]
    assert sorted(actual) == sorted(expected), 'ac: ' + str(actual) + ' ex: ' + str(expected)

    my_row = [-1, -1, -1]
    my_constraints = [1]
    actual = get_row_variations(my_row, my_constraints)
    expected = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    assert sorted(actual) == sorted(expected), 'ac: ' + str(actual) + ' ex: ' + str(expected)

    my_row = [0, 0, 0]
    my_constraints = [1]
    actual = get_row_variations(my_row, my_constraints)
    expected = []
    assert sorted(actual) == sorted(expected), 'ac: ' + str(actual) + ' ex: ' + str(expected)

    my_row = [0, 0, -1, 1, 0]
    my_constraints = [3]
    actual = get_row_variations(my_row, my_constraints)
    expected = []
    assert sorted(actual) == sorted(expected), 'ac: ' + str(actual) + ' ex: ' + str(expected)

    my_row = [0, 0, -1, 1, 0]
    my_constraints = [2]
    actual = get_row_variations(my_row, my_constraints)
    expected = [[0, 0, 1, 1, 0]]
    assert sorted(actual) == sorted(expected), 'ac: ' + str(actual) + ' ex: ' + str(expected)

    my_row = [0, 0, 1, 1, 0]
    my_constraints = [2]
    actual = get_row_variations(my_row, my_constraints)
    expected = [[0, 0, 1, 1, 0]]
    assert sorted(actual) == sorted(expected), 'ac: ' + str(actual) + ' ex: ' + str(expected)


def check_intersection():
    my_rows = [[0, 0, 1], [0, 1, 1], [0, 0, 1]]
    actual = get_intersection_row(my_rows)
    expected = [0, -1, 1]
    assert actual == expected, 'ac: ' + str(actual) + ' ex: ' + str(expected)

    my_rows = [[0, 1, -1], [-1, -1, -1]]
    actual = get_intersection_row(my_rows)
    expected = [-1, -1, -1]
    assert actual == expected, 'ac: ' + str(actual) + ' ex: ' + str(expected)


# check_get_combos()
# check_intersection()
# row_const = [[3], [0,1], []]
# col_const = [[2], [1,1], [1]]
# solve_easy_nonogram([row_const, col_const])

my_row = [-1] * 2
my_constraints = []
actual = get_row_variations(my_row, my_constraints)

print(len(actual))
print(count_row_variations(3, my_constraints))
