"""排行榜分页：并列名次、稳定排序、分页缓存与版本失效。

缺陷：同分按插入顺序而不是玩家名、并列名次用连续排名、缓存不随分数变化失效、
越界页返回脏数据、每次取页都重新全量排序。
"""


class Board:
    """排行榜分页台账。"""

    def __init__(self, page_size):
        self.page_size = page_size
        self.scores = {}
        self.revision = 0
        self.cache = {}
        self.scanned = 0

    def set_score(self, player, score):
        self.scores[player] = score
        self.revision += 1

    def page(self, index):
        """返回第 index 页（从 0 开始）的 (名次, 玩家, 分数)。"""
        self.scanned += len(self.scores)
        if index in self.cache:
            return self.cache[index]
        ordered = sorted(self.scores.items(), key=lambda item: -item[1])
        start = index * self.page_size
        rows = []
        for offset, (player, score) in enumerate(ordered[start:start + self.page_size]):
            rows.append((start + offset + 1, player, score))
        self.cache[index] = rows
        return rows

    def scanned_count(self):
        return self.scanned
