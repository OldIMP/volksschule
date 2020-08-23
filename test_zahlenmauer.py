# pylint: disable=missing-docstring
from argparse import Namespace
from zahlenmauer import sum_pair, sum_up, parse_range


def test_sum_pair():
    assert [6, 12] == sum_pair([2, 4, 8])


def test_sum_up():
    assert sum_up([2, 4, 8]) == 18


def test_parse_range_normal():
    args = Namespace()
    args.stop = 2
    args.symmetric = False
    assert [1, 2] == list(parse_range(args))


def test_parse_range_symmetric():
    args = Namespace()
    args.stop = 2
    args.symmetric = True
    assert [1, 2, 1] == list(parse_range(args))
