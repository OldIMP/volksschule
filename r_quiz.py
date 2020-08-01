"""Rechen-Quiz

Randomly generates a mix of math quizzes for the elementary school:
- +/- quizzes between 1-100
- Einmaleins: Multiply/division quizzes w/ product/divident up to 10

Output will be written to a txt file defined by --path to simplify printing
"""

import os
import random


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


def print_group(ratio_plus_minus, target_file, count, col):
    """Print a group of R Quiz to target_file"""
    quizzes = set()

    while len(quizzes) <= count:
        if random.random() > ratio_plus_minus:
            quizzes.add(MulDivQuiz())
        else:
            if random_bool():
                quizzes.add(PlusQuiz())
            else:
                quizzes.add(MinusQuiz())

    for _ in range(count // col):
        for _ in range(col):
            print(quizzes.pop(), end="=\t", file=target_file)
        print(file=target_file)


if __name__ == "__main__":
    import argparse

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
        "(default=r_quiz.txt in the working directory)",
        default="r_quiz.txt",
    )

    GROUP = PARSER.add_argument_group("Formatting")
    GROUP.add_argument(
        "-g",
        "--groups",
        help="No. of groups to be printed (default=6)",
        default=6,
        type=int,
    )
    GROUP.add_argument(
        "--count-per-group",
        help="No. of quizzes per group (default=30)",
        default=30,
        type=int,
    )
    GROUP.add_argument(
        "-c", "--columns", help="No. of columns (default=6)", default=6, type=int
    )

    ARGS = PARSER.parse_args()

    with open(ARGS.path, "w", encoding="utf-8") as file:
        for _ in range(ARGS.groups):
            print_group(ARGS.ratio_plus_minus, file, ARGS.count_per_group, ARGS.columns)
            print(file=file)
    print(f"written to {os.path.abspath(ARGS.path)}")
