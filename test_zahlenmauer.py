# pylint: disable=missing-docstring
from zahlenmauer import sum_pair, sum_up


def test_sum_pair():
    assert [6, 12] == sum_pair([2, 4, 8])


def test_sum_up():
    assert sum_up([2, 4, 8]) == 18
