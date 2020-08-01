# pylint: disable=missing-docstring

import random
from r_quiz import PlusQuiz, MinusQuiz, MulDivQuiz


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


def test_minus():
    minus_1 = MinusQuiz()
    minus_1.substrahend = 1
    minus_1.minuend = 2

    minus_2 = MinusQuiz()
    minus_2.substrahend = 2
    minus_2.minuend = 1

    assert minus_1 != minus_2

    quizzes = set()
    quizzes.add(minus_1)
    quizzes.add(minus_2)

    assert len(quizzes) == 2


def test_mul_div():
    random.seed(42)
    mul_1 = MulDivQuiz()
    mul_1.left = 2
    mul_1.right = 3

    assert str(mul_1) == "2⋅3"

    random.seed(0)
    div = MulDivQuiz()
    div.left = 2
    div.right = 3

    assert str(div) == "6:2"

    random.seed(42)
    mul_2 = MulDivQuiz()
    mul_2.left = 3
    mul_2.right = 2

    assert str(mul_2) == "3⋅2"

    assert mul_1 == mul_2 == div

    quizzes = set()
    quizzes.add(mul_1)
    quizzes.add(mul_2)
    quizzes.add(div)

    assert len(quizzes) == 1
