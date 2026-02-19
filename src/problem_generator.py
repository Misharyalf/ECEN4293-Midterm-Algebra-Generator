"""
Problem Generator Module
Generates algebra problems and converts them to root-finding form f(x) = 0.
"""

import random
import math


def generate_linear():
    """
    Generate a linear equation of the form:
        a*x + b = c

    Internally converts to root-finding form:
        f(x) = a*x + b - c
    """

    # Generate coefficients
    a = random.randint(1, 5)
    b = random.randint(-10, 10)
    c = random.randint(-10, 10)

    def f(x):
        return a * x + b - c

    equation_str = f"{a}x + {b} = {c}"

    return {
        "equation_str": equation_str,
        "f": f,
        "type": "linear"
    }


def generate_quadratic():
    """
    Generate a quadratic equation of the form:
        a*x^2 + b*x + c = 0
    """

    a = random.randint(1, 5)
    b = random.randint(-10, 10)
    c = random.randint(-10, 10)

    def f(x):
        return a * x**2 + b * x + c

    equation_str = f"{a}x^2 + {b}x + {c} = 0"

    return {
        "equation_str": equation_str,
        "f": f,
        "type": "quadratic"
    }


def generate_problem(problem_type=None):
    """
    Generate a problem based on requested type.
    If no type is specified, randomly choose.
    """

    if problem_type == "linear":
        return generate_linear()

    if problem_type == "quadratic":
        return generate_quadratic()

    # Random selection if not specified
    choice = random.choice(["linear", "quadratic"])

    if choice == "linear":
        return generate_linear()

    return generate_quadratic()
