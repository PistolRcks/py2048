import unittest
from game import Board

class TestBoardPrivate(unittest.TestCase):

    def test_compress(self):
        board = Board(4, 4)
        start = [2, 0, 4, 0]
        end_backward = [2, 4, 0, 0]
        end_forward = [0, 0, 2, 4]
        self.assertEqual(end_backward, board._Board__compress(start, 'left'))
        self.assertEqual(end_forward, board._Board__compress(start, 'right'))
        self.assertEqual(end_backward, board._Board__compress(start, 'up'))
        self.assertEqual(end_forward, board._Board__compress(start, 'down'))

    def test_combine(self):
        board = Board(4, 4)
        start_single = [2, 2, 0, 0]
        start_double = [2, 2, 4, 4]
        end_single = [4, 0, 0, 0]
        end_double = [4, 0, 8, 0]
        self.assertEqual(end_single, board._Board__combine(start_single))
        self.assertEqual(end_double, board._Board__combine(start_double))

    
    def test_set(self):
        board = Board(4, 4)
        end = [
            1, 0, 0, 0,
            0, 0, 0, 0,
            0, 0, 0, 0,
            0, 0, 0, 0
        ]
        board._Board__set(0, 0, 1)
        self.assertEqual(end, board.grid)

    def test_get_range(self):
        start = [
            1, 2, 3, 4,
            5, 6, 7, 8,
            9, 10, 11, 12,
            13, 14, 15, 16 
        ]
        row_first = [1, 2, 3, 4]
        row_last = [13, 14, 15, 16]
        col_first = [1, 5, 9, 13]
        col_last = [4, 8, 12, 16]
        board = Board(4, 4, start)
        self.assertEqual(row_first, board._Board__get_range(0, 'left'))
        self.assertEqual(row_first, board._Board__get_range(0, 'right'))
        self.assertEqual(row_last, board._Board__get_range(3, 'left'))
        self.assertEqual(row_last, board._Board__get_range(3, 'right'))
        self.assertEqual(col_first, board._Board__get_range(0, 'up'))
        self.assertEqual(col_first, board._Board__get_range(0, 'down'))
        self.assertEqual(col_last, board._Board__get_range(3, 'up'))
        self.assertEqual(col_last, board._Board__get_range(3, 'down'))


if __name__ == '__main__':
    unittest.main()


