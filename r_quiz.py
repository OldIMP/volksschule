"""Rechen-Quiz

Randomly generates a mix of math quizzes for the elementary school:
- +/- quizzes between 1-100
- Einmaleins: Multiply/division quizzes w/ product/divident up to 10

Output will be written to a pdf file defined by --path
"""

import random
import numpy as np


def random_bool():
    """Generate a random boolean"""
    return bool(random.getrandbits(1))


class NoOrderQuiz:
    """Base class for quiz where order doesn't matter"""

    def __init__(self, start, stop):
        self.left = random.randrange(start, stop)
        self.right = random.randrange(start, stop)

    def __eq__(self, other):
        if isinstance(other, type(self)):
            this_no_order = set((self.left, self.right))
            other_no_order = set((other.left, other.right))
            return this_no_order == other_no_order
        return NotImplemented

    def __hash__(self):
        return hash(tuple(sorted((self.left, self.right))))


class MulDivQuiz(NoOrderQuiz):
    # pylint: disable=too-few-public-methods
    """A mul/div quiz"""

    def __init__(self):
        super().__init__(2, 10)

    def __str__(self):
        if random_bool():
            return f"{self.left}⋅{self.right}"
        return f"{self.left*self.right}:{self.left}"


class PlusQuiz(NoOrderQuiz):
    # pylint: disable=too-few-public-methods
    """A + quiz"""

    def __init__(self):
        super().__init__(1, 100)

    def __str__(self):
        return f"{self.left}+{self.right}"


class MinusQuiz:
    """A minus quiz"""

    def __init__(self):
        self.subtrahend = random.randrange(2, 100)
        self.minuend = random.randrange(1, self.subtrahend)

    def __eq__(self, other):
        if isinstance(other, MinusQuiz):
            if self.subtrahend == other.subtrahend:
                return self.minuend == other.minuend
        return NotImplemented

    def __hash__(self):
        return hash((self.subtrahend, self.minuend))

    def __str__(self):
        return f"{self.subtrahend}-{self.minuend}"


def produce_matrix(ratio_plus_minus):
    "Produce a 2d matrix of quizzes"

    col = 12
    row = 38

    quizzes = set()

    while len(quizzes) < row * col:
        if random.random() > ratio_plus_minus:
            quizzes.add(MulDivQuiz())
        else:
            if random_bool():
                quizzes.add(PlusQuiz())
            else:
                quizzes.add(MinusQuiz())

    return np.char.array([f"{q}=" for q in quizzes]).reshape(row, col).tolist()


if __name__ == "__main__":
    import argparse
    import os
    from reportlab.platypus import SimpleDocTemplate, Table

    PARSER = argparse.ArgumentParser()

    PARSER.add_argument(
        "--ratio-plus-minus",
        help="ratio of +/- quizzes (default=0.4, i.e. 40%% of quizzes will be +/-)",
        default=0.4,
        type=float,
    )
    PARSER.add_argument(
        "-P",
        "--path",
        help="where the output will be saved, existing file will be overwritten "
        "(default=r_quiz.pdf in the working directory)",
        default="r_quiz.pdf",
    )
    ARGS = PARSER.parse_args()

    SimpleDocTemplate(ARGS.path).build([Table(produce_matrix(ARGS.ratio_plus_minus))])
    print(f"Written to {os.path.abspath(ARGS.path)}")
