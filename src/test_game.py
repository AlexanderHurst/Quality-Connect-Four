import game
import unittest


class TestGame(unittest.TestCase):

    def test_init(self):
        """Creates a game board and test that it is initialized correctly"""
        game_board = game.Board()
        self.assertEqual(game_board.dim, 7)
        self.assertFalse(game_board.playerTwo)
        self.assertFalse(game_board.winner)
        self.assertFalse(game_board.game_over)
        self.assertEqual(game_board.user_prompt,
                         "player 1 select a location: ")
        self.assertEqual(game_board.board,
                         [[0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0]]
                         )

        self.assertEqual(game_board.location_labels,
                         "| 1 | 2 | 3 | 4 | 5 | 6 | 7 | ")

    def test_string(self):
        """Tests string representation of the board"""
        game_board = game.Board(3)

        self.assertEqual(str(
            game_board), "|---+---+---|\n| 0 | 0 | 0 | \n| 0 | 0 | 0 | \n| 0 | 0 | 0 | \n|---+---+---|")

    def test_move(self):
        """tests placing tokens on the board"""
        game_board = game.Board()

        res = game_board.move(5)
        self.assertEqual(res, 0)
        self.assertEqual(game_board.board[0][4], 1)
        self.assertTrue(game_board.playerTwo)
        self.assertEqual(game_board.user_prompt,
                         "player 2 select a location: ")

        res = game_board.move(5)
        self.assertEqual(res, 0)
        self.assertEqual(game_board.board[1][4], 2)
        self.assertFalse(game_board.playerTwo)
        self.assertEqual(game_board.user_prompt,
                         "player 1 select a location: ")

        res = game_board.move("test")
        self.assertEqual(res, 1)
        res = game_board.move("")
        self.assertEqual(res, 1)

        res = game_board.move(float(9))
        self.assertEqual(res, 2)

        res = game_board.move(5)
        res = game_board.move(5)
        res = game_board.move(5)
        res = game_board.move(5)
        res = game_board.move(5)
        res = game_board.move(5)
        self.assertEqual(res, 3)

    def test_full_board(self):
        """test filling the board with no winners"""
        game_board = game.Board()

        for i in range(7):
            game_board.move(1)
            game_board.move(2)
            game_board.move(4)
            game_board.move(3)
            game_board.move(5)
            game_board.move(6)
            game_board.move(7)
        self.assertTrue(game_board.game_over)
        self.assertFalse(game_board.winner)

    def test_winners(self):
        """tests that player one and player two can win successfully"""
        p1_game_board = game.Board()

        for i in range(3):
            p1_game_board.move(1)
            p1_game_board.move(2)
        p1_game_board.move(1)

        self.assertTrue(p1_game_board.game_over)
        self.assertEqual(p1_game_board.winner, str(1))

        p2_game_board = game.Board()

        p2_game_board.move(7)
        for i in range(3):
            p2_game_board.move(1)
            p2_game_board.move(2)
        p1_game_board.move(1)

        self.assertTrue(p1_game_board.game_over)
        self.assertEqual(p1_game_board.winner, str(2))

    def test_winning_directions(self):
        """tests the different winning conditions
        ex.
        up
        right
        upright
        downright
        """
        up_game_board = game.Board()

        for i in range(3):
            up_game_board.move(1)
            up_game_board.move(2)
        up_game_board.move(1)

        self.assertTrue(up_game_board.game_over)
        self.assertEqual(up_game_board.winner, str(1))

        right_game_board = game.Board()

        for i in range(3):
            right_game_board.move(i+1)
            right_game_board.move(i+1)
        right_game_board.move(4)

        self.assertTrue(right_game_board.game_over)
        self.assertEqual(right_game_board.winner, str(1))

        up_right_game_board = game.Board()

        for i in range(4):
            up_right_game_board.move(i+1)

        for i in range(3):
            up_right_game_board.move(i+2)

        up_right_game_board.move(7)

        for i in range(2):
            up_right_game_board.move(i+3)

        up_right_game_board.move(4)

        self.assertTrue(up_right_game_board.game_over)
        self.assertEqual(up_right_game_board.winner, str(1))


if __name__ == "__main__":
    unittest.main()
