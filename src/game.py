class Board:

    def __init__(self):
        self.board = [[0 for x in range(8)] for i in range(8)]
        self.playerTwo = False

    def __str__(self):
        return(str([row + "\n" for row in self.board]))


game_board = Board()

print(game_board)
print([x for x in range(1, 9)])

usr_prompt = "player " + \
    str(int(game_board.playerTwo) + 1) + " select a location:"
location = input(usr_prompt)
