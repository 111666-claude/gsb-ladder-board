"""命令行入口：跑排行榜样例。"""

import argparse

from .core import Board


def build_parser():
    parser = argparse.ArgumentParser(prog="ladder-board", description="排行榜分页")
    parser.add_argument("--sample", default="tie", help="tie / stale / cache / scan")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    if args.sample == "tie":
        board = Board(page_size=10)
        board.set_score("bob", 100)
        board.set_score("amy", 100)
        rows = board.page(0)
        print("ranks=%d,%d first=%s" % (rows[0][0], rows[1][0], rows[0][1]))
    elif args.sample == "stale":
        board = Board(page_size=10)
        board.set_score("bob", 100)
        board.page(0)
        board.set_score("bob", 500)
        print("score=%d" % board.page(0)[0][2])
    elif args.sample == "cache":
        board = Board(page_size=10)
        for index in range(3000):
            board.set_score("p-%04d" % index, index)
        board.page(0)
        board.page(0)
        print("scanned=%d" % board.scanned_count())
    elif args.sample == "scan":
        board = Board(page_size=10)
        for index in range(3000):
            board.set_score("p-%04d" % index, index)
        for index in range(3000):
            board.page(index % 30)
        print("scanned=%d" % board.scanned_count())
    else:
        raise SystemExit("需要 --sample tie|stale|cache|scan")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
