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


class RankingTest(unittest.TestCase):
    def test_tied_scores_share_min_rank(self):
        board = Board(10)
        board.set_score("bob", 100)
        board.set_score("amy", 100)
        board.set_score("zed", 50)
        rows = board.page(0)
        self.assertEqual([row[0] for row in rows], [1, 1, 3])

    def test_tied_scores_sort_by_player_id_ascending(self):
        board = Board(10)
        board.set_score("bob", 100)
        board.set_score("amy", 100)
        rows = board.page(0)
        self.assertEqual([row[1] for row in rows], ["amy", "bob"])

    def test_ranks_monotonic_and_match_global_order(self):
        board = Board(3)
        scores = {"p%d" % index: (index * 7) % 5 for index in range(10)}
        for player, score in scores.items():
            board.set_score(player, score)
        rows = board.page(0) + board.page(1) + board.page(2) + board.page(3)
        self.assertEqual([row[0] for row in rows], sorted(row[0] for row in rows))
        expected = sorted(scores.items(), key=lambda item: (-item[1], item[0]))
        self.assertEqual([(row[1], row[2]) for row in rows], expected)


class PaginationTest(unittest.TestCase):
    def test_out_of_range_page_returns_empty(self):
        board = Board(10)
        board.set_score("bob", 10)
        self.assertEqual(board.page(1), [])
        self.assertEqual(board.page(99), [])

    def test_negative_page_returns_empty(self):
        board = Board(10)
        board.set_score("bob", 10)
        self.assertEqual(board.page(-1), [])

    def test_full_and_partial_pages(self):
        board = Board(2)
        for index in range(5):
            board.set_score("p%d" % index, index)
        self.assertEqual(len(board.page(0)), 2)
        self.assertEqual(len(board.page(2)), 1)
        self.assertEqual(board.page(3), [])


class CacheTest(unittest.TestCase):
    def test_score_change_invalidates_cached_page(self):
        board = Board(10)
        board.set_score("bob", 100)
        board.page(0)
        board.set_score("bob", 500)
        self.assertEqual(board.page(0)[0][2], 500)

    def test_new_player_invalidates_cached_page(self):
        board = Board(10)
        board.set_score("bob", 100)
        self.assertEqual(board.page(0)[0][1], "bob")
        board.set_score("amy", 200)
        self.assertEqual(board.page(0)[0][1], "amy")

    def test_repeat_fetch_same_version_does_not_rescan(self):
        board = Board(10)
        for index in range(100):
            board.set_score("p%03d" % index, index)
        board.page(0)
        scanned = board.scanned_count()
        for _ in range(10):
            self.assertEqual(board.page(0), board.page(0))
        self.assertEqual(board.scanned_count(), scanned)


if __name__ == "__main__":
    unittest.main()
