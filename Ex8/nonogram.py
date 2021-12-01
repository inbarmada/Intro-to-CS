############################################################
# FILE : nonogram.py
# WRITER : Inbar Leibovich , inbarlei , 21395389
# EXERCISE : intro2cse Ex8 2020
# DESCRIPTION: Solve nonograms
# STUDENTS I DISCUSSED THE EXERCISE WITH:
# WEB PAGES I USED:
# NOTES: For function get_intersection_row, when some row
#        variations for a given position had the same value
#        (black/white) and others were neutral, I left the
#        square neutral. I did this because if even a few
#        squares were neutral, it means that the given
#        position could go either way - either black or
#        white, so it wouldn't make sense to already choose
#        its color.
############################################################

def get_row_variations(row, blocks):
    """ Get all possible variations of the row given
    its current shading and its constraints """
    # Block sum will hold the number of squares that must be
    # to the right of the starting square for the next block
    block_sums = []
    num_blocks = len(blocks)
    for ind in range(num_blocks):
        if ind == 0:
            block_sums.insert(0, blocks[num_blocks - ind - 1])
        else:
            block_sums.insert(0, blocks[num_blocks - ind - 1] + 1)
            block_sums[0] += block_sums[1]
    block_sums.append(0)

    # Li will hold all possible variations
    li = []
    # Calculates variations and adds to li
    get_combos(row, block_sums, row[:], 0, 0, li)
    return li


def set_to_zeros(row, result, index, li):
    """ Once constraints are completed, set rest of row to 0s """
    # Iterate through remaining squares
    for i in range(index, len(row)):
        # If the square contains a 1, this variation is invalid; return
        if row[i] == 1:
            return
        # If legal to do so, set square to 0
        else:
            result[i] = 0
    # If all squares have been set to 0, the sequence
    # is valid; add to list
    li.append(result)
    return


def get_combos(row, block_sums, result, index, block_index, li):
    """ Get all possible variations of the row starting from index """
    # If finished constraints, set rest of row to 0s
    if block_index == len(block_sums) - 1:
        set_to_zeros(row, result, index, li)
    # If enough spaces left to complete the row according to the constraints
    elif index + block_sums[block_index] <= len(row):
        # Try putting down a 1 in the next index
        if row[index] != 0:
            put_down_ones(row, block_sums, result[:], index, block_index, li)
        # Otherwise put down a 0 and move to next cell
        if row[index] != 1:
            result[index] = 0
            get_combos(row, block_sums, result, index + 1, block_index, li)


def put_down_ones(row, block_sums, result, index, block_index, li):
    """ Fill next block with 1s """
    # Get number of cells in next block
    n = block_sums[block_index] - block_sums[block_index + 1]
    # If the cell after the block needs to be empty
    if block_sums[block_index + 1] != 0:
        n -= 1
        # Check whether the cell after the block can have a 0
        if row[index + n] == 1:
            return
        else:
            result[index + n] = 0

    # Check whether you can put in ones for the whole block
    broken = False
    for i in range(n):
        if row[index + i] != 0:
            result[index + i] = 1
        else:
            broken = True
            break

    # If successful, move on to next block
    if not broken:
        if block_sums[block_index + 1] != 0:
            n += 1
        get_combos(row, block_sums, result, index + n, block_index + 1, li)


def get_intersection_row(rows):
    """ Get the intersection of several possibilities for a row """
    intersection = []
    # If there are not possibilities, return empty
    if len(rows) == 0:
        return intersection
    # Otherwise iterate over the cells of the rows
    for index in range(len(rows[0])):
        # Check if all cells of a given index are the same color
        color = -1
        broken = False
        for row in rows:
            if color == -1:
                color = row[index]
            if row[index] == -1 or row[index] != color:
                broken = True
                break
        # If they are the same color, add that color to intersection
        if not broken:
            intersection.append(color)
        # Otherwise add -1
        else:
            intersection.append(-1)
    return intersection


def row_from_constraints(row, constraints):
    """ Solve row from constraints """
    # Get all variations
    possibilities = get_row_variations(row, constraints)
    # Given there are variations, get intersection of variations
    if possibilities:
        return get_intersection_row(possibilities), len(possibilities) == 1
    # Otherwise return the row
    else:
        return row, len(possibilities) == 1


def all_rows_from_constraints(board, constraints, rows):
    """ Solve from row constraints"""
    # Iterate over rows
    for i, row_ind in enumerate(rows):
        # Get row constraints
        consts = constraints[0][row_ind]
        # Solve row and check if it is complete
        board[row_ind], row_complete = row_from_constraints(board[row_ind],
                                                            consts)
        # If row is complete, remove it from list
        if row_complete:
            del rows[i]


def all_cols_from_constraints(board, constraints, cols):
    """ Solve from column constraints """
    # Iterate over columns
    for i, col_ind in enumerate(cols):
        # Get column in an array
        get_col = []
        for row_ind in range(len(board)):
            get_col.append(board[row_ind][col_ind])
        # Get col constraints
        consts = constraints[1][col_ind]
        # Solve col and check if it is complete
        col_res, col_complete = row_from_constraints(get_col, consts)
        # Put solved array of the column back into the board
        for row_ind in range(len(board)):
            board[row_ind][col_ind] = col_res[row_ind]
        # If column is complete, remove it from list
        if col_complete:
            del cols[i]


def board_from_constraints(board, constraints, rows, cols):
    """ Solve board from constraints """
    # Iterate over rows
    all_rows_from_constraints(board, constraints, rows)

    # Iterate over columns
    all_cols_from_constraints(board, constraints, cols)


# Only check rows/cols that contain -1s
def solve_easy_nonogram(constraints):
    """ Return the solution to a board, given it is unique """
    # Hold the indices of the rows and columns
    rows = list(range(len(constraints[0])))
    cols = list(range(len(constraints[1])))

    # Build board
    board = []
    for _ in rows:
        board.append([-1 for _ in cols])
    prev_board = []

    # While board is still changing
    while board != prev_board:
        prev_board = deep_copy(board)
        # Solve board from constraints
        board_from_constraints(board, constraints, rows, cols)

    return board


def solve_nonogram(constraints):
    """ Return all possible boards that match the constraints """
    board = solve_easy_nonogram(constraints)
    rows = list(range(len(constraints[0])))
    cols = list(range(len(constraints[1])))
    board_list = []
    board_possibilities(board, constraints, rows, cols, board_list)
    return board_list


def board_possibilities(board, constraints, rows, cols, board_list):
    """ Return all possibilities for the
    correct completion of a given board """
    # Duplicate arrays so you can change them
    rows = rows[:]
    cols = cols[:]
    prev_board = []

    # Fill in as much as possible of the board
    while board != prev_board:
        prev_board = deep_copy(board)
        board_from_constraints(board, constraints, rows, cols)
    # If there is a -1 on the board, change it to 0 and 1 on new boards
    chng = change(board, rows, cols)
    if chng:
        # Add the new boards to board_list
        board_possibilities(chng[0], constraints, rows, cols, board_list)
        board_possibilities(chng[1], constraints, rows, cols, board_list)
    # If there is no -1, check board and add to board_list
    else:
        if check(board, constraints):
            board_list.append(board)


def change(board, rows, cols):
    """ If board contains -1, duplicate the board and change
    the first square with -1 to 0 and 1 on each of the two
    boards, and return them. Otherwise return False """
    # Iterate over cells of board
    for row_ind in rows:
        for col_ind in cols:
            # If a cell is equal to -1
            if board[row_ind][col_ind] == -1:
                # Duplicate the board
                board_one = deep_copy(board)
                # Put a 0 in one copy
                board[row_ind][col_ind] = 0
                # Put a 1 in the other copy
                board_one[row_ind][col_ind] = 1
                # Return both copies
                return board, board_one
    # If no -1s are found, return False
    return False


def check(board, constraints):
    """ Check that board fits all the constraints """
    # Check that board fits row constraints
    if not check_rows(board, constraints[0]):
        return False

    # Flip rows and columns
    b = []
    for c in range(len(board[0])):
        new_row = []
        for r in range(len(board)):
            new_row.append(board[r][c])
        b.append(new_row)

    # Check that board fits column constraints
    if not check_rows(b, constraints[1]):
        return False

    # If board is valid, return True
    return True


def check_rows(board, constraints):
    """ Check that the rows of the board
    match the constraints given """
    # Iterate through rows in board
    for index, row in enumerate(board):
        # Get the constraints of the row
        c = constraints[index]

        # Check that row contains blocks in c, separated by spaces
        block_check = check_blocks(row, c)
        if block_check is not False:
            cur_ind = block_check
        else:
            return False

        # While there are cells remaining, make sure they are white
        while cur_ind < len(row):
            if row[cur_ind] != 0:
                return False
            cur_ind += 1

    # If the function succeeded, return True
    return True


def check_blocks(row, c):
    """ Check that row contains blocks in c, separated by spaces """
    # Iterate over cells in the row, starting at index 0
    cur_ind = 0
    # Iterate through the blocks in the constraints
    for block in c:
        # Check that the block is preceded by a white space
        if row[cur_ind] != 0 and cur_ind != 0:
            return False
        # Skip the white spaces
        while row[cur_ind] == 0:
            cur_ind += 1
        # Check that the next n cells are black,
        # where n is the length of the next block
        for i in range(block):
            if cur_ind >= len(row) or row[cur_ind] != 1:
                return False
            cur_ind += 1

    # If succeeded, return cur_ind
    return cur_ind


def deep_copy(mat):
    """ Copy mat into a new matrix and return it"""
    res = []
    for i in range(len(mat)):
        row = []
        for j in range(len(mat[i])):
            row.append(mat[i][j])
        res.append(row)
    return res


def count_row_variations(length, blocks, row=None):
    """ Count the number of variations possible on
    a row given its length and constraints """
    # Row is None or is empty
    if not row or check_empty(row):
        return count_empty_row_variations(length, blocks)
    elif sum(blocks) > length:
        return 0
    else:
        count_sum = 0
        # Find a one or zero and split the row
        for cur_ind in range(len(row)):
            if row[cur_ind] == 0:
                count_sum += split_zero(cur_ind, blocks, row)
                break

            elif row[cur_ind] == 1:
                count_sum += split_one(cur_ind, blocks, row)
                break
        return count_sum


def split_zero(cur_ind, blocks, row):
    """ Split the row around the 0 and solve for each side """
    count_sum = 0
    # Iterate through blocks to divide put
    # some in part one and others in part two
    for b in range(len(blocks) + 1):
        # Get part one
        part_one = count_row_variations(cur_ind,
                                        blocks[:b],
                                        row[:cur_ind])
        # Get part two
        part_two = count_row_variations(len(row) - cur_ind - 1,
                                        blocks[b:],
                                        row[cur_ind + 1:])
        # Add to sum
        count_sum += part_one * part_two
    return count_sum


def split_one(cur_ind, blocks, row):
    """ Split the row around the 1 and solve for each side """
    count_sum = 0
    # Decide which block will contain the 1
    for i in range(len(blocks)):
        # Decide on starting point for block
        range_start = cur_ind - blocks[i] + 1
        # Iterate through possible starting points
        for start_block in range(range_start, cur_ind + 1):
            # Find the end of the block
            end_block = start_block + blocks[i]
            # Calculate split and add to sum if exists
            split = calculate_split(row, blocks, start_block, end_block, i)
            if split:
                count_sum += split
    return count_sum


def calculate_split(row, blocks, start_block, end_block, i):
    """ Calculate a split around a block """
    # Check that there is enough space on both sides of the cut
    if start_block > sum(blocks[:i]) + i - 1 and len(row) - end_block + 1 \
            > sum(blocks[i + 1:]) + (len(blocks) - (i + 1)):
        # Check that there can be a 0 on sides of block if needed
        if end_block == len(row) or row[end_block] != 1:
            if start_block == 0 or row[start_block - 1] != 1:
                # Check block itself can be all 1s
                if block_between(start_block, end_block, row):
                    # Calculate left split
                    part_one = 1 if start_block == 0 else \
                        count_row_variations(start_block - 1, blocks[:i],
                                             row[:start_block - 1])
                    # Calculate right split
                    part_two = 1 if end_block == len(row) else \
                        count_row_variations(len(row[end_block + 1:]),
                                             blocks[i + 1:],
                                             row[end_block + 1:])
                    # Return results
                    return part_one * part_two


def block_between(start_block, end_block, row):
    """ Check that you can put a block between start_block and end_block """
    length = len(row)
    for i in range(start_block, end_block):
        if 0 < i < length and row[i] == 0:
            return False
    return True


def check_empty(row):
    """ Check if a row is empty """
    for c in row:
        if c != -1:
            return False
    return True


def count_empty_row_variations(length, blocks):
    """ Count variations of an empty row """
    # Empty row
    if len(blocks) == 0:
        return 1

    # Count black squares
    black = 0
    for i in blocks:
        black += i
    # Calculate number of spaces
    spaces = length - black

    if spaces - len(blocks) + 1 < 0:
        return 0

    # Calculate variations
    num = factorial(spaces - len(blocks) + 1, spaces + 1)
    num /= factorial(1, len(blocks))

    return num


def factorial(lower, n):
    """ Compute the result of (n! / lower!) - in other words,
    multiply all numbers between lower + 1 and n (inclusive)"""
    fac = n
    for i in range(lower + 1, n):
        fac *= i
    return fac
