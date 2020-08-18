############################################################
# FILE : nonogram.py
# WRITER : Inbar Leibovich , inbarlei , 21395389
# EXERCISE : intro2cse Ex8 2020
# DESCRIPTION: Solve nonograms
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
            res = put_down_ones(row, block_sums, result[:],
                                index, block_index, li)
            if res:
                combos.append(res)
        if row[index] != 1:
            res = put_down_a_zero(row, block_sums, result[:],
                                  index, block_index, li)
            if res:
                combos.append(res)
        return combos


def put_down_ones(row, block_sums, result, index, block_index, li):
    n = block_sums[block_index] - block_sums[block_index + 1]
    if block_sums[block_index + 1] != 0:
        n -= 1

        # If after n blocks is a 1, try moving up one
        if row[index + n] == 1:
            return []
        else:
            result[index + n] = 0

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

        return get_combos(row, block_sums, result,
                          index + n, block_index + 1, li)


def put_down_a_zero(row, block_sums, result, index, block_index, li):
    result[index] = 0
    return get_combos(row, block_sums, result, index + 1, block_index, li)


# Must write a note at top of page
def get_intersection_row(rows):
    intersection = []
    if len(rows) == 0:
        return intersection
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


def row_from_constraints(row, constraints):
    possibilities = get_row_variations(row, constraints)
    if possibilities:
        return get_intersection_row(possibilities), len(possibilities) == 1
    else:
        return row


def board_from_constraints(board, constraints, rows, cols):
    # Evaluate for rows
    for i, row_ind in enumerate(rows):
        consts = constraints[0][row_ind]
        board[row_ind], row_complete = row_from_constraints(board[row_ind], consts)
        if row_complete:
            del rows[i]

    # Evaluate for columns
    for i, col_ind in enumerate(cols):
        get_col = []
        for row_ind in range(len(board)):
            get_col.append(board[row_ind][col_ind])
        consts = constraints[1][col_ind]
        col_res, col_complete = row_from_constraints(get_col, consts)
        for row_ind in range(len(board)):
            board[row_ind][col_ind] = col_res[row_ind]
        if col_complete:
            del cols[i]


# Only check rows/cols that contain -1s
def solve_easy_nonogram(constraints):
    num_rows = len(constraints[0])
    num_cols = len(constraints[1])
    rows = list(range(num_rows))
    cols = list(range(num_cols))

    # Build board
    board = []
    for i in rows:
        board.append([-1 for j in cols])
    prev_board = []

    while board != prev_board:
        prev_board = deep_copy(board)

        board_from_constraints(board, constraints, rows, cols)
    return board


def solve_nonogram(constraints):
    nono = solve_easy_nonogram(constraints)
    rows = list(range(len(constraints[0])))
    cols = list(range(len(constraints[1])))
    return board_possibilities(nono, constraints, rows, cols)


def board_possibilities(board, constraints, rows, cols):
    rows = rows[:]
    cols = cols[:]
    prev_board = []

    while board != prev_board:
        prev_board = deep_copy(board)
        board_from_constraints(board, constraints, rows, cols)

    board_list = []
    chng = change(board, rows, cols)
    if chng:
        board_list.extend(board_possibilities(chng[0], constraints,
                                              rows, cols))
        board_list.extend(board_possibilities(chng[1], constraints,
                                              rows, cols))
    else:
        if check(board, constraints):
            board_list.append(board)

    return board_list


def change(board, rows, cols):
    for row_ind in rows:
        for col_ind in cols:
            if board[row_ind][col_ind] == -1:
                board_one = deep_copy(board)
                board[row_ind][col_ind] = 0
                board_one[row_ind][col_ind] = 1
                return board, board_one
    return False


def check(board, constraints):
    # Check that board fits row constraints
    if not check_rows(board, constraints[0]):
        return False

    # Flip columns and rows
    b = []
    for c in range(len(board[0])):
        new_row = []
        for r in range(len(board)):
            new_row.append(board[r][c])
        b.append(new_row)

    # Check that board fits column constraints
    if not check_rows(b, constraints[1]):
        return False

    # If board fits return True
    return True


def check_rows(board, constraints):
    for index, row in enumerate(board):
        cur_ind = 0
        c = constraints[index]
        for block in c:
            while row[cur_ind] == 0:
                cur_ind += 1
            for i in range(block):
                if cur_ind >= len(row) or row[cur_ind] != 1:
                    return False
                cur_ind += 1
        while cur_ind < len(row):
            if row[cur_ind] != 0:
                return False
            cur_ind += 1
    return True


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

my_row = [-1, -1, 1, -1, 1, -1, -1, -1, 0, -1]
my_constraints = [2, 2, 1]
actual = get_row_variations(my_row, my_constraints)
# expected = [[0, 0, 1, 1, 1]]
# print(actual)
# assert sorted(actual) == sorted(expected), 'ac: ' + str(actual) + ' ex: ' + str(expected)

# check_get_combos()
# check_intersection()

unknown_nonogram = [[
    [2, 18],
    [1, 20],
    [23],
    [23],
    [24],
    [25],
    [25],
    [19, 4],
    [14, 3, 4],
    [13, 6, 3],
    [11, 8, 3],
    [12, 2, 2, 3],
    [7, 2, 3],
    [5, 3, 3, 3],
    [4, 1, 1, 1, 1, 1, 1, 3],
    [4, 1, 3, 3, 1, 3],
    [4, 1, 2, 2, 1, 1, 1],
    [1, 2, 2, 1, 1],
    [1, 2, 4, 1, 3, 1],
    [1, 1 ,1, 2],
    [1, 1, 1, 1],
    [2, 13, 3],
    [3, 1, 3, 1],
    [1, 3, 12, 1, 1],
    [5, 10, 2, 1],
    [6, 8, 2, 1],
    [7, 5, 2, 1],
    [3, 3],
    [3, 3],
    [15]
],
    [
        [17, 4],
        [15, 2, 3],
        [19, 5],
        [1, 19, 5],
        [13, 4],
        [13, 2],
        [13, 3, 1, 2, 1],
        [12, 1, 1, 3, 1, 1],
        [12, 4, 1, 1, 2, 3],
        [12, 1, 2, 1, 1, 3, 2],
        [12, 2, 1, 4, 2],
        [10, 1, 1, 4, 1],
        [10, 1, 1, 4, 1],
        [9, 3, 1, 4, 1],
        [8, 3, 1, 1, 4, 1],
        [11, 2, 1, 3, 2],
        [11, 2, 1, 3, 2],
        [11, 1, 2, 1, 4, 3],
        [8, 2, 4, 1, 3, 2, 1],
        [7, 3, 1, 1, 2, 3, 1],
        [7, 2, 3, 2, 1],
        [9, 6],
        [18, 1],
        [15, 3],
        [16, 4]
    ]]



print(solve_easy_nonogram(unknown_nonogram))

