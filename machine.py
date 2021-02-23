import random
import copy


class Machine:

    def __init__(self, m_tile, u_tile):
        self.m_tile = m_tile
        self.u_tile = u_tile

    # method that returns the throw number or the tiles position
    def throw_state(self, count, tile, board):
        tiles = 0
        positions = []

        for idx, row in enumerate(board):
            for idx2, col in enumerate(row):
                if board[idx][idx2] == tile:
                    if count:
                        tiles += 1
                    else:
                        positions.append([idx, idx2])
        if count:
            result = tiles
        else:
            result = positions

        return result

    def cell_tile(self, board, cell, searching):
        for idx, row in enumerate(board):
            for idx2, col in enumerate(row):
                if idx == cell[0] and idx2 == cell[1]:
                    if searching:
                        return col
                    else:
                        board[idx][idx2] = self.m_tile
                        return board

    def machine_move(self, board):                      # each move is a different approach for the current situation
        corners = [[0, 0], [2, 2], [0, 2], [2, 0]]      # corners are decisive in this game
        move_type = self.evaluation(board)              # get the strategy needed

        if type(move_type) is not int:                          # placing to third blank cell when two tiles are inline
            board = self.cell_tile(board, move_type, False)
        elif move_type == 1:
            board = self.defense(board, corners)                # avoiding user strategies
        elif move_type == 2:
            board = self.strategy_1(board, corners)             # three path fork using three corners
        elif move_type == 3:
            board = self.strategy_2(board, corners)             # three path fork using two corners and the center
        elif move_type == 4:
            found, board = self.winning_branch(board, "0", [])  # looks for winning single paths

        return board

    def winning_branch(self, board, index, tree):
        state = self.board_state(board, False, None)
        if state is not False:
            first_index = index[1]
            first_index = "0" + first_index
            first_level = tree[0]

            for idx, branch in first_level.items():
                if idx == first_index:
                    selected_branch = branch
                    found = True
                    return found, selected_branch
        elif state is False and self.finished(board) is True:
            selected_branch = tree[0]["01"]
            found = True
            return found, selected_branch

        branches = self.move_options(board, index)
        tree.append(branches)
        for index, branch in branches.items():
            found, selected_branch = self.winning_branch(branch, index, tree)
            if found:
                return found, selected_branch

    def move_options(self, board, index):
        branches = {}
        base = index
        i = 1
        for row in range(3):
            for cell in range(3):
                if board[row][cell] == " ":
                    copy_matrix = copy.deepcopy(board)
                    copy_matrix[row][cell] = self.m_tile
                    j = str(i)
                    index = base + j
                    branches[index] = copy_matrix
                    i += 1
        return branches

    # strategy steps: 1.random corner, 2.opposite corner as 1, 3.third corner (better without adjacent user tiles)
    def strategy_1(self, board, corners):
        new_cell = []
        for corner in corners:  # loop through corners
            if self.cell_tile(board, corner, True) == self.m_tile:  # when there's a tile in a corner
                for coord in corner:                                # looks for the opposite cell coordinates
                    if coord == 0: new_cell.append(2)
                    else: new_cell.append(0)
                opposite = self.cell_tile(board, new_cell, True)    # finds out if the cell is empty
                if opposite == " ":                                 # if it is, machine places the tile
                    board = self.cell_tile(board, new_cell, False)
                    return board
                elif opposite == self.m_tile:                       # if machine has already a tile there
                    available = []
                    for corner2 in corners:
                        if corner2 != corner and corner2 != opposite: # collect two other corners
                            available.append(corner2)
                        board = self.corner_path(board, available)
                        return board
                elif opposite == self.u_tile:                           # user tile in the opposite corner
                    for corner3 in corners:
                        if corner3 != corner and corner3 != new_cell:   # analyze two left corners
                            if self.cell_tile(board, corner3, True) == " ": # place tile in a corner per throw
                                board = self.cell_tile(board, corner3, False)
                                return board
        rand_num = random.randint(0, 3)  # if we haven't tiles in any corner
        selected = corners[rand_num]    # randomly
        board = self. cell_tile(board, selected, False)
        return board

    def corner_path(self, board, available):  # finds out if the row or column of the corner is a possible winning path
        for cell in available:  # analyze two corners
            row, col = cell
            blank = True
            for num in range(3):  # find out if row and column are empty
                if self.cell_tile(board, [row, num], True) != " ":
                    blank = False
                if self.cell_tile(board, [row, num], True) != " ":
                    blank = False
            if blank:
                if self.cell_tile(board, cell, True) == " ":  # if it is, place tile there
                    board = self.cell_tile(board, cell, False)
                    return board
        rand_num = random.randint(0, 1)  # random corner if doesn't find
        if self.cell_tile(board, available[rand_num], True) == " ":
            board = self.cell_tile(board, available[rand_num], False)
            return board

    def strategy_2(self, board, corners):
        if self.cell_tile(board, [1, 1], True) == " ":  # first throw of the strategy: the center
            board = self.cell_tile(board, [1, 1], False)
            return board
        else:                   # usually the second throw depends on the user tile position (corner or not)
            last_throw = None
            m_corner = []
            own_pos = self.throw_state(False, self.m_tile, board)   # get machine positions to watch the status
            for pos in own_pos:
                if pos in corners:                          # if there's a tile in a corner, there's only one move left
                    last_throw = True
                    m_corner = pos
            if last_throw:
                row_corner, col_corner = [], []                # collect consecutive corners
                for corner in corners:
                    if corner != m_corner:
                        if m_corner[0] == corner[0]:   # by consecutive, I mean that share column or row (not opposite)
                            row_corner = corner
                        elif m_corner[1] == corner[1]:
                            col_corner = corner
                if self.cell_tile(board, [row_corner[0], 1], True) == " ": # the cell between corners should be empty
                    board = self.cell_tile(board, row_corner, False)
                    return board
                elif self.cell_tile(board, [1, col_corner[1]], True) == " ":
                    board = self.cell_tile(board, col_corner, False)
                    return board
                else:                           # if both "middle cells" are full, random corner and wait for the tie
                    rand_corner = random.randint(0, 1)
                    possible_corners = [row_corner, col_corner]
                    board = self.cell_tile(board, possible_corners[rand_corner], False)
                    return board
            else:                   # this part of the code is the second move of the strategy
                is_corner = False
                position = []
                user_pos = self.throw_state(False, self.u_tile, board)  # extract user positions

                if user_pos[0] in corners:
                    is_corner = True            # find out if position is a corner
                    position = user_pos[0]      # exact position of the corner
                if is_corner:
                    opposite = []               # if it is, find opposite corner
                    for coord in position:
                        if coord == 0: opposite.append(2)
                        elif coord == 2: opposite.append(0)
                    if self.cell_tile(board, opposite, True) == " ":    # if opposite corner is empty, place it there
                        board = self.cell_tile(board, opposite, False)
                        return board
                    else:
                        available = []                                  # if not, random empty corner
                        for corner in corners:
                            if corner != position[0] and corner != opposite:
                                available.append(corner)
                        board = self.corner_path(board, available)
                        return board

                else:                               # if the user tile isn't in a corner
                    row, col = user_pos[0]          # find position
                    rand = random.randint(1, 2)
                    if rand == 1: rand = 0          # place the tile in a random side of the user tile
                    if row == 1:
                        if self.cell_tile(board, [rand, col], True) == " ":
                            board = self.cell_tile(board, [rand, col], False)
                        else:
                            board = self.corner_path(board, corners)
                    elif col == 1:
                        if self.cell_tile(board, [row, rand], True) == " ":
                            board = self.cell_tile(board, [row, rand], False)
                    return board

    def defense(self, board, corners):
        throw = self.throw_state(True, self.m_tile, board)

        if throw == 0:                                          # first machine throw as "O" (user first)

            center = False
            if self.cell_tile(board, [1, 1], True) == " ":      # found out if middle cell is empty
                center = True

            if center:
                board = self.cell_tile(board, [1, 1], False)    # if it is, place the tile there

            else:    # if it isn't, means user tile is there
                rand_num = random.randint(0, 3)
                corner = corners[rand_num]
                board = self.cell_tile(board, corner, False)    # place it in a random corner

            return board

        elif throw == 1:        # if in the second machine move there isn't danger, seal the defense and force tie
            own_pos = self.throw_state(False, self.m_tile, board)
            machine_row, machine_col = own_pos[0]                           # find machine position
            if own_pos[0] in corners:
                for corner in corners:
                    corner_row, corner_col = corner                             # and it's nearest corners
                    if corner_row == machine_row or corner_col == machine_col:  # adjacent corners share row or column
                        if self.cell_tile(board, corner, True) == " ":
                            board = self.cell_tile(board, corner, False)
                            return board
            else:
                rand_num = random.randint(0, 3)
                corner = corners[rand_num]
                board = self.cell_tile(board, corner, False)  # place it in a random corner

        return board

    # analyzes each possible approach by importance and chooses the correct for the situation
    def evaluation(self, board):
        # danger r:last blank cell inline, 1.defense, 2.strategy1, 3.strategy2, 4.other

        danger = self.board_state(board, True, self.u_tile)   # danger: two user tiles inline
        if danger is not False:
            return danger                                     # return: last blank cell inline (list)

        throw = self.throw_state(True, self.m_tile, board)    # get the throw number
        if self.m_tile == "O":                                # defense: when the user begins
            if throw == 0 or throw == 1:                      # only one or two throws are needed to block strategies
                return 1

        elif throw < 3 and self.m_tile == "X":                # forks: when machine begins, in three steps are completed
            rand_num = random.randint(2, 3)                   # choose one randomly
            return 3

        else:                                                 # other situations
            return 4

    # normal board analyzes rows, the transpose matrix analyzes columns and a self made board with diagonals as rows
    def board_state(self, board, danger, tile):  # it can search for danger (two match) or for victory (three match)
        aes, bes, ces = [], [], []

        for row in board:               # transposing matrix
            a, b, c = row
            aes.append(a)
            bes.append(b)
            ces.append(c)
        transpose = [aes, bes, ces]     # columns

        diagonal = [[board[0][0], board[1][1], board[2][2]], [board[0][2], board[1][1], board[2][0]]]

        def result(tile):  # analyzes all lines of the 3 boards (3 ways to do the match)
            row_result = self.line_state(board, tile, danger)
            column_result = self.line_state(transpose, tile, danger)
            diagonal_result = self.line_state(diagonal, tile, danger)

            if danger:
                # columns and diagonals coordinates are different as the board is changed
                if row_result is not False:
                    return row_result               # for rows is the normal board, where we play
                elif column_result is not False:
                    idx, idx2 = column_result       # for columns, the coordinates are reversed
                    column_result = [idx2, idx]
                    return column_result
                elif diagonal_result is not False:
                    # for diagonals, there's a copy of diagonal board, but with the coordinates referring those cells
                    diagonal_coord = [[[0, 0], [1, 1], [2, 2]], [[0, 2], [1, 1], [2, 0]]]
                    diagonal_result = diagonal_coord[diagonal_result[0]][diagonal_result[1]]
                    return diagonal_result
                else:
                    return False
            else:   # in case we're looking for victory, just returns true or false
                results = [row_result, column_result, diagonal_result]
                if True in results: return True
                else: return False

        if danger:  # looking for danger in every line
            block = result(tile)
            if block is not False: return block
        else:
            win1 = result(self.u_tile)
            win2 = result(self.m_tile)
            if win1: return self.u_tile     # returns winning tile
            if win2: return self.m_tile
        return False

    # method that looks for danger or victory by lines
    def line_state(self, board, tile, danger):

        for idx, row in enumerate(board):
            counter = 0     # accumulator that looks for X or O in the same line
            blank = None    # saves the blank cell coordinate in a dangerous situation (two same tiles in line)
            for idx2, cell in enumerate(row):
                if cell == tile:
                    counter += 1
                else:
                    if cell == " ":                 # if the situation is dangerous, there's only one empty cell
                        blank = [idx, idx2]         # and is saved here
                if counter == 2 and danger and blank is not None:
                    return blank                    # returns coordinates of the blank cell
                else:                               # if danger is False, it looks for victory
                    if counter == 3 and danger is False:
                        return True
        return False

    def finished(self, board):
        finished = True

        for row in board:           # loop though the board
            for cell in row:
                if cell == " ":     # when finds a blank cell, finished turns False
                    finished = False

        return finished
