import unittest
from game import Board

class TestBoard(unittest.TestCase):

    def test_combine_left(self):
        start = [
            1, 1, 0, 0,
            1, 0, 1, 0,
            1, 0, 0, 1,
            0, 0, 1, 1
        ]

        end = [
            2, 0, 0, 0,
            2, 0, 0, 0,
            2, 0, 0, 0,
            2, 0, 0, 0
        ]

        board = Board(4, 4, start)
        board.move('left')

        self.assertEqual(end, board.grid)

    def test_combine_right(self):
        start = [
            0, 0, 1, 1,
            0, 1, 0, 1,
            1, 0, 0, 1,
            1, 1, 0, 0
        ]

        end = [
            0, 0, 0, 2,
            0, 0, 0, 2,
            0, 0, 0, 2,
            0, 0, 0, 2
        ]

        board = Board(4, 4, start)
        board.move('right')

        self.assertEqual(end, board.grid)

    def test_combine_up(self):
        start = [
            1, 1, 1, 0,
            1, 0, 0, 0,
            0, 1, 0, 1,
            0, 0, 1, 1
        ]

        end = [
            2, 2, 2, 2,
            0, 0, 0, 0,
            0, 0, 0, 0,
            0, 0, 0, 0
        ]

        board = Board(4, 4, start)
        board.move('up')

        self.assertEqual(end, board.grid)

    def test_combine_down(self):
        start = [
            0, 0, 1, 1,
            0, 1, 0, 1,
            1, 0, 0, 0,
            1, 1, 1, 0
        ]

        end = [
            0, 0, 0, 0,
            0, 0, 0, 0,
            0, 0, 0, 0,
            2, 2, 2, 2
        ]

        board = Board(4, 4, start)
        board.move('down')

        self.assertEqual(end, board.grid)

    def test_double_combine(self):
        start = [
            1, 1, 1, 1,
            1, 1, 2, 2,
            2, 2, 1, 1,
            0, 0, 0, 0
        ]

        end = [
            2, 2, 0, 0,
            2, 3, 0, 0,
            3, 2, 0, 0,
            0, 0, 0, 0
        ]

        board = Board(4, 4, start)
        board.move('left')

        self.assertEqual(end, board.grid)


    def test_new_tile(self):
        start = [
            0, 0, 0, 0,
            0, 0, 0, 0,
            0, 0, 0, 0,
            0, 0, 0, 0
        ]

        board = Board(4, 4)

        self.assertEqual(start, board.grid)
        
        board.new_tile()

        self.assertNotEqual(start, board.grid)


if __name__ == '__main__':
    unittest.main()


