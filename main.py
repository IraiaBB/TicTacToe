from machine import Machine
from user import User


class Main:

    def __init__(self):
        self.game()

    def game(self):
        board = [[" ", " ", " "],  # this is the grid
                 [" ", " ", " "],
                 [" ", " ", " "]]
        finished = False        # determines whether the board is full or not
        win = False             # turns to True when there's a tree match

        u = User()
        user_tile = u.choose_tile()  # the user decides between X and O

        if user_tile == "X":
            machine_tile = "O"  # assigning tile-player
            user_turn = True

        else:
            machine_tile = "X"
            user_turn = False


        m = Machine(machine_tile, user_tile)

        # the game is finished when someone wins or when the board is full
        while finished is False and win is False:

            if user_turn:  # meanwhile, players take turns
                board = u.user_move(board, user_tile)  # user move
                name = "User"
                user_turn = False

            else:
                board = m.machine_move(board)   # machine move
                name = "Machine"
                user_turn = True

            print(name, "turn: ")

            for row in board:  # print the board
                print(row)

            # this method returns a tile when someone wins, otherwise it returns "-" (tie)
            winner_tile = m.board_state(board, False, None)

            if winner_tile == "X" or winner_tile == "O":  # checking if there's a winner
                win = True
                print(name, "has won! Congrats :)")

            else:  # checking if the board is full
                finished = m.finished(board)

            if finished is True and win is False:
                print("It's a tie")

        print("End of game")  # checking end of loop


p = Main()

