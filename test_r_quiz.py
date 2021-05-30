# pylint: disable=missing-docstring

import pytest
import numpy as np
from r_quiz import PlusQuiz, MinusQuiz, MulQuiz, DivQuiz, produce_matrix, Layout


def test_produce_matrix():
    count = Layout.SIMPLE.col * Layout.SIMPLE.row
    matrix = np.char.array(produce_matrix(0.1, False))
    plus_minus = matrix.count("+") + matrix.count("-")

    assert plus_minus.sum() < count / 2
    assert matrix.size == matrix.count("=").sum() == count


@pytest.mark.parametrize("quiz", [PlusQuiz(), MinusQuiz(), MulQuiz(), DivQuiz()])
def test_str_simple(quiz):
    simple_str = quiz.str()

    assert "\n" not in simple_str
    assert simple_str.endswith("=")


def test_str_simple_mul():
    assert "⋅" in MulQuiz().str()


@pytest.mark.parametrize("quiz, operator", [(PlusQuiz(), "+"), (MinusQuiz(), "-")])
def test_str_schriftlich_plus_minus(quiz, operator):
    schriftlich = quiz.str(True)
    lines = schriftlich.splitlines()
    expected_len = quiz.max_len + 1

    assert len(lines) == 3
    assert all(len(line) == expected_len for line in lines)

    assert schriftlich.startswith(" ")
    assert lines[1].startswith(operator)
    assert lines[2] == "-" * expected_len


def test_str_schriftlich_mul():
    lines = MulQuiz().str(True).splitlines()

    assert len(lines) == 2
    assert (line_len := len(lines[0])) == len(lines[1])

    assert lines[1] == "-" * line_len


def test_str_div_quiz_eq():
    quiz = DivQuiz()
    assert quiz.str() == quiz.str(False) == quiz.str(True)
