# pylint: disable=missing-docstring

import numpy as np
from r_quiz import PlusQuiz, MulQuiz, produce_matrix


def test_plus():
    plus_1 = PlusQuiz()
    plus_1.left = 1
    plus_1.right = 2

    plus_2 = PlusQuiz()
    plus_2.left = 2
    plus_2.right = 1

    assert plus_1 == plus_2

    quizzes = set()
    quizzes.add(plus_1)
    quizzes.add(plus_2)

    assert len(quizzes) == 1


def test_mul():
    mul_1 = MulQuiz()
    mul_1.left = 2
    mul_1.right = 3

    assert str(mul_1) == "2⋅3"

    mul_2 = MulQuiz()
    mul_2.left = 3
    mul_2.right = 2

    assert str(mul_2) == "3⋅2"

    assert mul_1 == mul_2

    quizzes = set()
    quizzes.add(mul_1)
    quizzes.add(mul_2)

    assert len(quizzes) == 1


def test_produce_matrix():
    count = 12 * 38
    matrix = np.char.array(produce_matrix(0.1))
    plus_minus = matrix.count("+") + matrix.count("-")

    assert plus_minus.sum() < count / 2
    assert matrix.size == matrix.count("=").sum() == count
