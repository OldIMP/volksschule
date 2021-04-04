"""Rechen-Quiz

Randomly generates a mix of math quizzes for the elementary school:
- +/- quizzes
- Multiply/division quizzes

Output will be written to a pdf file defined by --path
"""

import random
from dataclasses import dataclass
import numpy as np

BLANK_WIDTH = 50
COL = 3
ROW = 27

PLUS_MINUS_MAX = 100000
MUL_RESULT_MAX = 10000


def random_bool():
    """Generate a random boolean"""
    return bool(random.getrandbits(1))


class NoOrderQuiz:
    """Base class for quiz where order doesn't matter"""

    left: int
    right: int

    def __init__(self, one, the_other):
        if random_bool():
            self.left = one
            self.right = the_other
        else:
            self.left = the_other
            self.right = one

    def __eq__(self, other):
        if isinstance(other, type(self)):
            this_no_order = set((self.left, self.right))
            other_no_order = set((other.left, other.right))
            return this_no_order == other_no_order
        return NotImplemented

    def __hash__(self):
        return hash(tuple(sorted((self.left, self.right))))


@dataclass(frozen=True)
class OrderQuiz:
    """Base class for quiz where order matters"""

    left: int
    right: int


class PlusQuiz(NoOrderQuiz):
    # pylint: disable=too-few-public-methods
    """A + quiz"""

    def __init__(self):
        super().__init__(
            random.randrange(1, PLUS_MINUS_MAX), random.randrange(1, PLUS_MINUS_MAX)
        )

    def __str__(self):
        return f"{self.left}+{self.right}"


class MinusQuiz(OrderQuiz):
    # pylint: disable=too-few-public-methods
    """A - quiz"""

    def __init__(self):
        minuend = random.randrange(2, PLUS_MINUS_MAX)
        super().__init__(minuend, random.randrange(1, minuend))

    def __str__(self):
        return f"{self.left}-{self.right}"


class MulQuiz(NoOrderQuiz):
    # pylint: disable=too-few-public-methods
    """A multiply quiz"""

    def __init__(self):
        one_digit_factor = random.randrange(2, 10)
        super().__init__(
            one_digit_factor, random.randrange(2, MUL_RESULT_MAX // one_digit_factor)
        )

    def __str__(self):
        return f"{self.left}⋅{self.right}"


class DivQuiz(OrderQuiz):
    # pylint: disable=too-few-public-methods
    """A division quiz"""

    def __init__(self):
        super().__init__(random.randrange(2, 9), random.randrange(2, 9))

    def __str__(self):
        return f"{self.left*self.right}:{self.left}"


def produce_quizzes(count, ratio_plus_minus):
    """Produce a set of quizzes w/ size of count"""

    quizzes = set()

    while len(quizzes) < count:
        if random.random() > ratio_plus_minus:
            if random_bool():
                quizzes.add(MulQuiz())
            else:
                quizzes.add(DivQuiz())
        else:
            if random_bool():
                quizzes.add(PlusQuiz())
            else:
                quizzes.add(MinusQuiz())

    return quizzes


def produce_matrix(ratio_plus_minus):
    "Produce a 2d matrix of quizzes"

    count = ROW * COL
    quizzes = produce_quizzes(count, ratio_plus_minus)

    return np.char.array([f"{q}=" for q in quizzes]).reshape(ROW, COL).tolist()


if __name__ == "__main__":
    import argparse
    import os
    from reportlab.platypus import SimpleDocTemplate, Table
    from reportlab.lib import colors

    def positive_float(arg):
        "Parses arg as a postive float"
        flt = float(arg)
        if flt <= 0:
            raise argparse.ArgumentTypeError(f"{arg} is not postive")
        return flt

    PARSER = argparse.ArgumentParser()

    PARSER.add_argument(
        "--ratio-plus-minus",
        help="ratio of +/- quizzes (default=0.4, i.e. 40%% of quizzes will be +/-)",
        default=0.4,
        type=positive_float,
    )
    PARSER.add_argument(
        "-P",
        "--path",
        help=(
            "where the output will be saved, existing file will be overwritten"
            " (default=r_quiz.pdf in the working directory)"
        ),
        default="r_quiz.pdf",
    )
    ARGS, _ = PARSER.parse_known_args()

    DATA = produce_matrix(ARGS.ratio_plus_minus)
    STYLE = [
        ("SIZE", (0, 0), (-1, -1), 16),
        ("RIGHTPADDING", (0, 0), (-1, -1), BLANK_WIDTH),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]

    INTERVAL = 30 // COL
    LINE = 0
    while LINE < ROW:
        LINE += INTERVAL
        STYLE.append(("LINEABOVE", (0, LINE), (-1, LINE), 1, colors.black))

    SimpleDocTemplate(ARGS.path).build([Table(DATA, style=STYLE)])
    print(f"Written to {os.path.abspath(ARGS.path)}")
