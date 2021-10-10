"""Rechen-Quiz

Randomly generates a mix of math quizzes for the elementary school:
- +/- quizzes
- Multiply/division quizzes

Output will be written to a pdf file defined by --path
"""

import abc
import random
from dataclasses import dataclass
from enum import Enum
import numpy as np

PLUS_MINUS_MAX = 1_000_000
MUL_RESULT_MAX = 10_000
QUIZ_PER_GROUP = 15


def random_bool():
    """Generate a random boolean"""
    return bool(random.getrandbits(1))


@dataclass(frozen=True)
class OrderQuiz(abc.ABC):
    """Base class for quiz where order matters"""

    left: int
    right: int

    @abc.abstractmethod
    def str(self, schriftlich=False) -> str:
        """
        Returns the str representation of the quiz.

        Parameters
        ----------
        schriftlich : bool, default False
            False to print a simple form e.g. '1+1='
            True to print a 'schriftlich' form, e.g.
                  1
                +12
                ---
        """
        raise NotImplementedError

    @property
    def max_len(self) -> int:
        "Max len of left & right"
        return max(len(str(self.left)), len(str(self.right)))


class NoOrderQuiz(OrderQuiz):
    # Intermediate ABC
    # pylint: disable=W0223
    """Base class for quiz where order doesn't matter"""

    def __init__(self, one, the_other):
        if random_bool():
            super().__init__(one, the_other)
        else:
            super().__init__(the_other, one)

    def __eq__(self, other):
        if isinstance(other, type(self)):
            this_no_order = set((self.left, self.right))
            other_no_order = set((other.left, other.right))
            return this_no_order == other_no_order
        return NotImplemented

    def __hash__(self):
        return hash(tuple(sorted((self.left, self.right))))


class PlusQuiz(NoOrderQuiz):
    # pylint: disable=too-few-public-methods
    """A + quiz"""

    def __init__(self):
        super().__init__(
            random.randrange(1, PLUS_MINUS_MAX), random.randrange(1, PLUS_MINUS_MAX)
        )

    def str(self, schriftlich=False) -> str:
        if schriftlich:
            return f""" {str(self.left).rjust(self.max_len)}
+{str(self.right).rjust(self.max_len)}
{'-'*(self.max_len+1)}"""

        return f"{self.left}+{self.right}="


class MinusQuiz(OrderQuiz):
    # pylint: disable=too-few-public-methods
    """A - quiz"""

    def __init__(self):
        minuend = random.randrange(2, PLUS_MINUS_MAX)
        super().__init__(minuend, random.randrange(1, minuend))

    def str(self, schriftlich=False) -> str:
        if schriftlich:
            return f""" {str(self.left).rjust(self.max_len)}
-{str(self.right).rjust(self.max_len)}
{'-'*(self.max_len+1)}"""

        return f"{self.left}-{self.right}="


class MulQuiz(NoOrderQuiz):
    # pylint: disable=too-few-public-methods
    """A multiply quiz"""

    def __init__(self):
        smaller_factor = random.randrange(2, 100)
        super().__init__(
            smaller_factor, random.randrange(2, MUL_RESULT_MAX // smaller_factor)
        )

    def str(self, schriftlich=False) -> str:
        quiz = f"{self.left}⋅{self.right}"
        return quiz + ("\n" + "-" * len(quiz) if schriftlich else "=")


class DivQuiz(OrderQuiz):
    # pylint: disable=too-few-public-methods
    """A division quiz"""

    def __init__(self):
        divisor = random.randrange(2, 9)
        super().__init__(random.randrange(divisor, 1000), divisor)

    def str(self, _=False) -> str:
        return f"{self.left}:{self.right}="


class Layout(Enum):
    """Contains info about the layout depending on the quiz form (schriftlich or not)"""

    SIMPLE = 3, 27
    SCHRIFTLICH = 6, 7

    def __init__(self, col: int, row: int):
        self.col = col
        self.row = row


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


def produce_matrix(ratio_plus_minus, schriftlich) -> list[str]:
    "Produce a 2d matrix of quizzes"

    layout = Layout.SCHRIFTLICH if schriftlich else Layout.SIMPLE
    count = layout.row * layout.col
    quizzes = produce_quizzes(count, ratio_plus_minus)

    quizzes_str = [q.str(schriftlich) for q in quizzes]
    return np.char.array(quizzes_str).reshape(layout.row, layout.col).tolist()


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
        "-S",
        "--schriftlich",
        help="produce quizzes in 'schriftlich' forms",
        action="store_true",
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

    DATA = produce_matrix(ARGS.ratio_plus_minus, ARGS.schriftlich)
    STYLE = [
        ("SIZE", (0, 0), (-1, -1), 16),
        ("RIGHTPADDING", (0, 0), (-1, -1), 20 if ARGS.schriftlich else 55),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 55 if ARGS.schriftlich else 10),
        # monospace necessary for schriftlich alignment
        ("FONTNAME", (0, 0), (-1, -1), "Courier"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]

    LAYOUT = Layout.SCHRIFTLICH if ARGS.schriftlich else Layout.SIMPLE
    INTERVAL = QUIZ_PER_GROUP // LAYOUT.col
    LINE = 0
    while LINE < LAYOUT.row:
        LINE += INTERVAL
        STYLE.append(("LINEABOVE", (0, LINE), (-1, LINE), 1, colors.black))

    SimpleDocTemplate(ARGS.path).build([Table(DATA, style=STYLE)])
    print(f"Written to {os.path.abspath(ARGS.path)}")
