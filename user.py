class User:

    def user_move(self, board, tile):
        empty_cell = False

        while not empty_cell:  # ask until a blank cell is picked
            row, col = self.ask_coord()

            if board[row][col] == " ":
                empty_cell = True  # a blank space in the matrix is an empty cell, so leaves the loop
                board[row][col] = tile
            else:
                print("This cell is not empty, choose another one")

        return board

    def ask_coord(self):

        print("Enter the coordinates")

        while True:
            row = input("Row:")
            col = input("Column:")

            try:
                row = int(row)  # casting from string to int
                col = int(col)
                break

            except TypeError:  # catching the error if the introduced value cannot be converted to int
                print("This is not an integer! Try again")

        return row, col

    def choose_tile(self):

        tile = input("Choose your tile: X or O. Remember: X always begins.")
        tile = tile.upper()     # assure that the tile is in capital letter

        while True:  # runs until a correct tile is introduced

            if tile == "X":
                print("You chose X")
                break   # ends the loop and returns the tile

            elif tile == "O":
                print("You chose O")
                break

            else:
                print("You have to write an 'x' or an 'o'")

            tile = input("Try again:")
            tile = tile.upper()

        return tile

