import shutil


class Board:
    def __init__(self, dim=7):
        """Creates a board object for connect four"""
        # number of columns in the board
        # must be greater than or equal to 4
        self.dim = dim
        # the dim x dim board
        self.board = [[0 for x in range(self.dim)] for i in range(self.dim)]

        # whether or not it is player twos turn
        self.playerTwo = False
        # who is the winner, false for none
        self.winner = False

        # Colours
        # Green for player one, Red for player two
        # Cyan for winning four in a row
        self.playerColour = ['\033[92m', '\033[91m']
        self.winColour = "\033[1;36m"
        self.colourReset = '\033[0m'

        # whether or not the game is over
        self.game_over = False

        # information for user
        self.user_prompt = ""
        self._set_user_prompt()

        # labels for columns, only works for dim < 10
        self.location_labels = "| "
        self.location_labels += ''.join("{0} | ".format(i)
                                        for i in range(1, self.dim + 1))

    def move(self, location):
        """Tries to place the users move into a given location

        On success this will also update the player, prompt
        and check the board for game over conditions

        Returns 0 for success
        Returns 1 if location is not an integer
        Returns 2 if location is outside the boundries
        Returns 3 if location is full
        """

        # attempt to parse the input to an int
        # if this raises a value error return 1
        try:
            location = int(location)
        except ValueError:
            return 1

        # return 2 if the location is out of bounds
        if location < 1 or location > self.dim:
            return 2

        # scan the column for the first empty space
        # and place the user move there
        # then update prompt and game status
        for row in self.board:
            if row[location - 1] == 0:
                row[location - 1] = int(self.playerTwo) + 1

                self.playerTwo = not self.playerTwo
                self._set_user_prompt()

                self.check_board()
                return 0
        # if unable to place the move then return 3
        return 3

    def _set_user_prompt(self):
        """Updates the user prompt based on the game state"""

        # if the game is not over update the player
        if self.game_over == False:
            self.user_prompt = "player " + \
                str(int(self.playerTwo) + 1) + " select a location: "

        # otherwise update the prompt with who won
        else:
            if self.winner == False:
                self.user_prompt = "Tie Game!"
            else:
                self.user_prompt = "The winner is: Player " + str(self.winner)

    def check_board(self):
        """Checks the board to determine if the game has a winner
        or if the board is full

        Updates the relevant information before exiting"""
        # for every space in the board if there is space
        # check up, upright, right, down right
        # for four moves from a given player in a row
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

                    # right update
                    if right_win:
                        for k in range(4):
                            self.board[i][j + k] = 'X'
                        self.game_over = True
                        self.winner = str(int(not self.playerTwo) + 1)
                        self._set_user_prompt()
                        return

                    # up update
                    if up_win:
                        for k in range(4):
                            self.board[i + k][j] = 'X'
                        self.game_over = True
                        self.winner = str(int(not self.playerTwo) + 1)
                        self._set_user_prompt()
                        return

                    # up right update
                    if up_right_win:
                        for k in range(4):
                            self.board[i + k][j + k] = 'X'
                        self.game_over = True
                        self.winner = str(int(not self.playerTwo) + 1)
                        self._set_user_prompt()
                        return

                    # down right update
                    if down_right_win:
                        for k in range(4):
                            self.board[i - k][j + k] = 'X'
                        self.game_over = True
                        self.winner = str(int(not self.playerTwo) + 1)
                        self._set_user_prompt()
                        return

        # no winners, ensure the board still has space
        for i in range(self.dim):
            if self.board[self.dim - 1][i] == 0:
                return
        self.game_over = True
        self._set_user_prompt()

    def __str__(self):
        """Generates the string representation for the board
        Including coulours and borders
        """
        # border for top and bottom of board
        top_bot_border = "|---" + "+---" * (self.dim - 1) + "|"
        temp = top_bot_border + "\n"

        # go through each row (in reverse so that board can be printed top to bottom)
        for row in reversed(self.board):
            temp += "| "
            # go through each number in each row (to apply any needed formatting)
            # and add each number and border to the temp string
            for num in row:
                if num == 0:
                    temp += str(num)
                elif num == 'X':
                    temp += self.winColour + num + self.colourReset
                else:
                    temp += self.playerColour[num - 1] + \
                        str(num) + self.colourReset
                temp += " | "

            temp += "\n"
        temp += top_bot_border
        return temp


if __name__ == "__main__":
    # create a game board with 7 spaces
    game_board = Board(7)
    # keep track of if the previous move failed and how
    move_success = 0

    # while the game is not over
    while (game_board.game_over == False):
        # clear the terminal every move
        terminal_size = shutil.get_terminal_size()
        print(terminal_size.lines * "\n")

        # inform the user of input errors
        if move_success == 1:
            print("Please enter an integer")
        if move_success == 2:
            print("Make sure you enter a number between 1 and {0}".format(
                game_board.dim))
        if move_success == 3:
            print("That column is full")

        # show the game board to the user
        # with column labels
        print(game_board)
        print(game_board.location_labels)

        # get the user input and attempt to add it to the board
        move_success = game_board.move(input(game_board.user_prompt))

    # clear the terminal
    terminal_size = shutil.get_terminal_size()
    print(terminal_size.lines * "\n")

    # print the board and winning information
    print(game_board)
    print(game_board.user_prompt)
