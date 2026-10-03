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


class RankingTest(unittest.TestCase):
    def test_tied_scores_share_min_rank(self):
        board = Board(10)
        board.set_score("amy", 100)
        board.set_score("bob", 100)
        board.set_score("cid", 50)
        rows = board.page(0)
        self.assertEqual([row[0] for row in rows], [1, 1, 3])

    def test_tied_scores_order_by_player_id(self):
        board = Board(10)
        board.set_score("bob", 100)
        board.set_score("amy", 100)
        rows = board.page(0)
        self.assertEqual([row[1] for row in rows], ["amy", "bob"])

    def test_ranks_are_monotonic_across_pages(self):
        board = Board(2)
        for name, score in [("a", 90), ("b", 90), ("c", 80), ("d", 70), ("e", 70)]:
            board.set_score(name, score)
        ranks = [row[0] for page in (board.page(0), board.page(1), board.page(2)) for row in page]
        self.assertEqual(ranks, sorted(ranks))
        self.assertEqual(ranks, [1, 1, 3, 4, 4])


class CacheTest(unittest.TestCase):
    def test_score_change_invalidates_cached_page(self):
        board = Board(10)
        board.set_score("bob", 100)
        self.assertEqual(board.page(0)[0][2], 100)
        board.set_score("bob", 500)
        self.assertEqual(board.page(0)[0][2], 500)

    def test_repeated_fetch_does_not_rescan(self):
        board = Board(10)
        for index in range(100):
            board.set_score("p-%03d" % index, index)
        board.page(0)
        scanned_after_first = board.scanned_count()
        for _ in range(50):
            board.page(0)
            board.page(1)
        self.assertEqual(board.scanned_count(), scanned_after_first)

    def test_repeated_fetch_returns_same_rows(self):
        board = Board(10)
        for index in range(30):
            board.set_score("p-%03d" % index, index)
        self.assertEqual(board.page(1), board.page(1))


class PagingTest(unittest.TestCase):
    def test_out_of_range_page_is_empty(self):
        board = Board(10)
        board.set_score("bob", 10)
        self.assertEqual(board.page(1), [])
        self.assertEqual(board.page(99), [])

    def test_negative_page_is_empty(self):
        board = Board(10)
        board.set_score("bob", 10)
        self.assertEqual(board.page(-1), [])

    def test_page_matches_global_order(self):
        board = Board(3)
        for index in range(10):
            board.set_score("p-%02d" % index, index * 7 % 13)
        merged = [row for page in (board.page(0), board.page(1), board.page(2), board.page(3)) for row in page]
        expected = sorted(board.scores.items(), key=lambda item: (-item[1], item[0]))
        self.assertEqual([(row[1], row[2]) for row in merged], expected)
