 

import random
import math


def _find_bracket(f, xl_start=-5.0, xu_start=5.0, max_expands=25):
     
    xl = float(xl_start)
    xu = float(xu_start)

    f_xl = f(xl)
    f_xu = f(xu)

    if f_xl == 0:
        return (xl, xl)
    if f_xu == 0:
        return (xu, xu)

    for _ in range(max_expands):
        if f_xl * f_xu < 0:
            return (xl, xu)

        width = xu - xl
        xl = xl - width
        xu = xu + width

        f_xl = f(xl)
        f_xu = f(xu)

        if f_xl == 0:
            return (xl, xl)
        if f_xu == 0:
            return (xu, xu)

    raise ValueError("Could not find a bracketing interval for this generated function")


def generate_linear():
    """
    Generate a linear equation of the form:
        a*x + b = c

    Internally converts to root-finding form:
        f(x) = a*x + b - c

    Returns a guaranteed bracket for bisection.
    """

    a = random.randint(1, 5)
    b = random.randint(-10, 10)
    c = random.randint(-10, 10)

    def f(x):
        return a * x + b - c

    equation_str = f"{a}x + {b} = {c}"

     
    root = (c - b) / a
    xl = root - 10.0
    xu = root + 10.0

    return {
        "equation_str": equation_str,
        "f": f,
        "type": "linear",
        "bracket": (xl, xu)
    }


def generate_quadratic():
     

    a = random.randint(1, 5)
    b = random.randint(-10, 10)
    c = random.randint(-10, 10)

    def f(x):
        return a * x**2 + b * x + c

    equation_str = f"{a}x^2 + {b}x + {c} = 0"

    bracket = _find_bracket(f)

    return {
        "equation_str": equation_str,
        "f": f,
        "type": "quadratic",
        "bracket": bracket
    }


def generate_problem(problem_type=None):
     

    if problem_type == "linear":
        return generate_linear()

    if problem_type == "quadratic":
        return generate_quadratic()

    choice = random.choice(["linear", "quadratic"])
    if choice == "linear":
        return generate_linear()

    return generate_quadratic()
