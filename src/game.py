class Board:
    def __init__(self, dim):
        self.dim = dim
        self.board = [[0 for x in range(self.dim)] for i in range(self.dim)]

        self.playerTwo = False
        self.user_prompt = ""
        self._set_user_prompt()

        self.game_over = False

        self.location_labels = "| "
        self.location_labels += ''.join("{0} | ".format(i)
                                        for i in range(1, self.dim + 1))

    def move(self, location):
        for row in self.board:
            if row[location - 1] == 0:
                row[location - 1] = int(self.playerTwo) + 1
                break

        self.playerTwo = not self.playerTwo
        self._set_user_prompt()

    def _set_user_prompt(self):
        self.user_prompt = "player " + \
            str(int(self.playerTwo) + 1) + " select a location: "

    def __str__(self):
        top_bot_border = "|---" + "+---" * (self.dim - 1) + "|"
        temp = top_bot_border + "\n"
        for row in reversed(self.board):
            temp += "| "
            for num in row:
                temp += str(num) + " | "
            temp += "\n"
        temp += top_bot_border
        return temp


game_board = Board(7)

while (game_board.game_over == False):
    print(game_board)
    print(game_board.location_labels)

    game_board.move(int(input(game_board.user_prompt)))

    print("\n\n\n")
