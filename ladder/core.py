"""排行榜分页：并列名次、稳定排序、分页缓存与版本失效。

排序按分数降序、同分按玩家 id 升序；同分共享最小名次。排序结果与页缓存
按版本失效：任何 set_score 之后下一次取页会重算，同一版本内重复取页
直接命中缓存，不重排。
"""


class Board:
    """排行榜分页台账。"""

    def __init__(self, page_size):
        self.page_size = page_size
        self.scores = {}
        self.revision = 0
        self.scanned = 0
        self._ordered = None
        self._pages = {}

    def set_score(self, player, score):
        self.scores[player] = score
        self.revision += 1
        self._ordered = None
        self._pages.clear()

    def _ensure_ordered(self):
        if self._ordered is not None:
            return
        self.scanned += len(self.scores)
        ordered = sorted(self.scores.items(), key=lambda item: (-item[1], item[0]))
        rows = []
        previous_score = None
        rank = 0
        for position, (player, score) in enumerate(ordered):
            if score != previous_score:
                rank = position + 1
                previous_score = score
            rows.append((rank, player, score))
        self._ordered = rows

    def page(self, index):
        """返回第 index 页（从 0 开始）的 (名次, 玩家, 分数)。"""
        if index < 0:
            return []
        start = index * self.page_size
        if start >= len(self.scores):
            return []
        if index in self._pages:
            return self._pages[index]
        self._ensure_ordered()
        rows = self._ordered[start:start + self.page_size]
        self._pages[index] = rows
        return rows

    def scanned_count(self):
        return self.scanned
