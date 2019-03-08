import shutil


class Board:
    def __init__(self, dim):
        self.dim = dim
        self.board = [[0 for x in range(self.dim)] for i in range(self.dim)]

        self.playerTwo = False
        self.playerColour = ['\033[92m', '\033[91m']
        self.colourReset = '\033[0m'

        self.user_prompt = ""
        self._set_user_prompt()

        self.game_over = False

        self.location_labels = "| "
        self.location_labels += ''.join("{0} | ".format(i)
                                        for i in range(1, self.dim + 1))

    def move(self, location):
        try:
            location = int(location)
        except ValueError:
            return 1

        if location < 1 or location > self.dim:
            return 2

        for row in self.board:
            if row[location - 1] == 0:
                row[location - 1] = int(self.playerTwo) + 1

                self.playerTwo = not self.playerTwo
                self._set_user_prompt()

                self.check_board()
                return 0

        return 3

    def _set_user_prompt(self):
        self.user_prompt = "player " + \
            str(int(self.playerTwo) + 1) + " select a location: "

    def check_board(self):
        for i in range(self.dim):
            for j in range(self.dim):
                temp = self.board[i][j]

                if temp != 0:

                    right_win = True
                    down_right_win = True
                    up_right_win = True
                    up_win = True

                    # if too far right
                    if j > self.dim - 4:
                        right_win = False
                        down_right_win = False
                        up_right_win = False

                    # if too far up
                    if i > self.dim - 4:
                        up_win = False
                        up_right_win = False

                    # if too far down
                    if i < 3:
                        down_right_win = False

                    for k in range(3):
                        # right check
                        if right_win:
                            if self.board[i][j + k + 1] != temp:
                                right_win = False

                        # up check
                        if up_win:
                            if self.board[i + k + 1][j] != temp:
                                up_win = False

                        # up right check
                        if up_right_win:
                            if self.board[i + k + 1][j + k + 1] != temp:
                                up_right_win = False

                        # down right check
                        if down_right_win:
                            if self.board[i - k - 1][j + k + 1] != temp:
                                down_right_win = False

                    if right_win or down_right_win or up_right_win or up_win:
                        print(up_win)
                        print(right_win)
                        print(up_right_win)
                        print(down_right_win)
                        self.game_over = True

    def __str__(self):
        top_bot_border = "|---" + "+---" * (self.dim - 1) + "|"
        temp = top_bot_border + "\n"
        for row in reversed(self.board):
            temp += "| "
            for num in row:
                if num == 0:
                    temp += str(num)
                else:
                    temp += self.playerColour[num - 1] + \
                        str(num) + self.colourReset
                temp += " | "

            temp += "\n"
        temp += top_bot_border
        return temp


game_board = Board(7)
move_success = 0
while (game_board.game_over == False):
    terminal_size = shutil.get_terminal_size()
    print(terminal_size.lines * "\n")

    if move_success == 1:
        print("Please enter an integer")
    if move_success == 2:
        print("Make sure you enter a number between 1 and {0}".format(
            game_board.dim))
    if move_success == 3:
        print("That column is full")

    print(game_board)
    print(game_board.location_labels)

    move_success = game_board.move(input(game_board.user_prompt))
