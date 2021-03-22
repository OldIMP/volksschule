# Volksschule
[![Python application](https://github.com/OldIMP/volksschule/actions/workflows/python-app.yml/badge.svg)](https://github.com/OldIMP/volksschule/actions/workflows/python-app.yml)
[![CodeQL](https://github.com/OldIMP/volksschule/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/OldIMP/volksschule/actions/workflows/codeql-analysis.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Python scripts for elementary school exercises in Austria (Volksschule) also as programming exercises for myself :P

## Zahlenmauer (`zahlenmauer.py`)
Caculates all possible [Zahlenmauer](https://de.wikipedia.org/wiki/Zahlenmauer) w/ bottom No. ranging from 1 to --stop, e.g.
`(1, 2, 3, 4, 5)->[3, 5, 7, 9]->[8, 12, 16]->[20, 28]->[48]`. See docstring or use `--help`

And yes, I know it's all just binomial coefficients, but hey I'm a programmer not a mathmatician ;)

## Rechen-Quiz (`r-quiz.py`)
Randomly generates a mix of math quizzes for the elementary school