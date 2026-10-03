import unittest

from ladder.core import Board


class BasicTest(unittest.TestCase):
    def test_empty_board(self):
        self.assertEqual(Board(10).page(0), [])

    def test_single_player_is_first(self):
        board = Board(10)
        board.set_score("bob", 10)
        self.assertEqual(board.page(0), [(1, "bob", 10)])

    def test_page_size_is_stored(self):
        self.assertEqual(Board(5).page_size, 5)

    def test_revision_starts_at_zero(self):
        self.assertEqual(Board(5).revision, 0)

    def test_scanned_starts_at_zero(self):
        self.assertEqual(Board(5).scanned_count(), 0)


if __name__ == "__main__":
    unittest.main()
