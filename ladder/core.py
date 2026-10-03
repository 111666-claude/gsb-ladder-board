"""排行榜分页：并列名次、稳定排序、分页缓存与版本失效。"""


class Board:
    """排行榜分页台账。"""

    def __init__(self, page_size):
        self.page_size = page_size
        self.scores = {}
        self.revision = 0
        self.cache = {}
        self.scanned = 0
        self._ordered = []
        self._ordered_revision = -1

    def set_score(self, player, score):
        self.scores[player] = score
        self.revision += 1

    def _ensure_ordered(self):
        """分数有变化才重排，并预计算并列名次、清空过期页缓存。"""
        if self._ordered_revision == self.revision:
            return
        self.scanned += len(self.scores)
        ordered = sorted(self.scores.items(), key=lambda item: (-item[1], item[0]))
        rows = []
        rank = 0
        previous_score = None
        for position, (player, score) in enumerate(ordered):
            if score != previous_score:
                rank = position + 1
                previous_score = score
            rows.append((rank, player, score))
        self._ordered = rows
        self._ordered_revision = self.revision
        self.cache.clear()

    def page(self, index):
        """返回第 index 页（从 0 开始）的 (名次, 玩家, 分数)，越界返回空列表。"""
        if index < 0:
            return []
        self._ensure_ordered()
        if index in self.cache:
            return self.cache[index]
        start = index * self.page_size
        rows = list(self._ordered[start:start + self.page_size])
        self.cache[index] = rows
        return rows

    def scanned_count(self):
        return self.scanned
