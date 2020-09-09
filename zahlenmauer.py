"""Zahlenmauer

Caculates all possible https://de.wikipedia.org/wiki/Zahlenmauer
 w/ bottom No. ranging from 1 to --stop, e.g.
(1, 2, 3, 4, 5)->[3, 5, 7, 9]->[8, 12, 16]->[20, 28]->[48]

Becareful since a big stop will take quite long,
e.g. --stop 9 will take several hours w/ following output:

...
There're 995 sums in total:
      bottom
sum
1280    1056
1259    1008
1301    1008
1177     992
1383     992
...      ...
1790      16
1810      16
1817      16
1830      16
1837      16

[995 rows x 1 columns]

"""

from itertools import chain, permutations, tee


def sum_pair(iterable):
    "s -> s0+s1, s1+s2, s2+s3, ..."
    left, right = tee(iterable)
    next(right, None)
    return [x + y for x, y in zip(left, right)]


def sum_up(row):
    "Sum up until there's only 1 No. & return it"
    next_row = sum_pair(row)
    if len(next_row) > 1:
        print(next_row, end="->")
        return sum_up(next_row)

    print(next_row)
    return next_row[0]


def parse_range(args):
    """
    Parse a range based on args.stop & args.symmetric, e.g.
    * args.stop=2, args.symmetric=False -> [1, 2]
    * args.stop=2, args.symmetric=True -> [1, 2, 1]
    """

    a_range = range(1, args.stop + 1)

    if args.symmetric:
        a_range = chain(a_range, range(args.stop - 1, 0, -1))

    return a_range


if __name__ == "__main__":
    import argparse
    import pandas as pd

    def parse_bottom():
        "Parse CLI arg as bottom stop"
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "-S",
            "--stop",
            help="largest No. in the bottom (default=5, min=2)",
            default=5,
            type=int,
        )
        parser.add_argument(
            "--symmetric",
            help="set to make the bottom symmetric e.g."
            " '-S 2 --symmetric' will produce [1, 2, 1]",
            action="store_true",
        )
        args, _ = parser.parse_known_args()
        if args.stop < 2:
            parser.error("stop must >= 2")
        return parse_range(args)

    BOTTOM_SUM = pd.DataFrame(columns=["bottom", "sum"])
    ALL_BOTTOMS = permutations(parse_bottom())

    for index, bottom in enumerate(ALL_BOTTOMS):
        print(bottom, end="->")
        BOTTOM_SUM.loc[index] = [bottom, sum_up(bottom)]

    print(f"There're {BOTTOM_SUM.nunique()['sum']} sums in total:")
    print(
        BOTTOM_SUM.groupby("sum")
        .count()
        .sort_values(["bottom", "sum"], ascending=[False, True])
    )
