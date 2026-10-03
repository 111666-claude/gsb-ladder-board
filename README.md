# ladder-board

排行榜分页：并列名次、稳定排序、分页缓存与版本失效，只用 Python 标准库。

```
python3 -m ladder.cli --sample tie
python3 -m ladder.cli --sample stale
python3 -m ladder.cli --sample cache
python3 -m ladder.cli --sample scan
python3 -m unittest discover -s tests -v
```

## 口径（README 为准）

- **排序**：分数降序，同分按玩家 id 升序。
- **并列名次**：同分共享最小名次（1,1,3 这种），不是连续名次。
- **分页**：每页 `page_size` 条，从 0 开始编号；越界页返回空列表。
- **缓存失效**：任何分数变化后，之前缓存的页必须重新计算，不许返回旧结果。
- **不变量**：同一份分数重复取页结果相同；名次单调不减；同页内容与全局排序一致。
- **代价**：同一版本内重复取页不许重排，`scanned_count` 不随取页次数线性增长。
- **规模**：10 万玩家、每秒 10 万次取页，单次摊还 O(page_size)。

## 输出契约（不改格式）

```
ranks=..,.. first=..
score=..
scanned=..
scanned=..
```

## 目录

```
ladder/core.py   排序、名次、分页与缓存
ladder/cli.py    命令行入口
tests/           unittest 用例
```
