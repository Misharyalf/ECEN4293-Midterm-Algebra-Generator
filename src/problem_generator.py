import random
import math
import sympy as sp

def _find_bracket(f, xl_start=-5.0, xu_start=5.0, max_expands=60):
    xl = float(xl_start)
    xu = float(xu_start)

    f_xl = f(xl)
    f_xu = f(xu)

    if not (math.isfinite(f_xl) and math.isfinite(f_xu)):
        raise ValueError("Non-finite function value during bracketing")

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

        if not (math.isfinite(f_xl) and math.isfinite(f_xu)):
            raise ValueError("Non-finite function value during bracketing")

        if f_xl == 0:
            return (xl, xl)
        if f_xu == 0:
            return (xu, xu)

    raise ValueError("Could not find a bracketing interval for this generated function")


def generate_linear():
    a = random.randint(1, 5)
    b = random.randint(-10, 10)
    c = random.randint(-10, 10)

    def f(x):
        return a * x + b - c

    equation_str = f"{a}x + {b} = {c}"
    root = (c - b) / a

    return {
        "mode": "single",
        "equation_str": equation_str,
        "f": f,
        "type": "linear",
        "bracket": (root - 10.0, root + 10.0)
    }


def generate_quadratic():
    a = random.randint(1, 5)
    r1 = random.randint(-8, 8)
    r2 = random.randint(-8, 8)
    while r2 == r1:
        r2 = random.randint(-8, 8)

    b = -a * (r1 + r2)
    c = a * (r1 * r2)

    def f(x):
        return a * x**2 + b * x + c

    equation_str = f"{a}x^2 + {b}x + {c} = 0"

    xl = min(r1, r2) - 2.0
    xu = max(r1, r2) + 2.0

    try:
        bracket = _find_bracket(f, xl_start=xl, xu_start=xu)
    except ValueError:
        bracket = _find_bracket(f)

    return {
        "mode": "single",
        "equation_str": equation_str,
        "f": f,
        "type": "quadratic",
        "bracket": bracket
    }




def generate_two_variable_solve_for_y():
    x = sp.Symbol("x")

    a = random.randint(1, 5)
    b = random.randint(1, 6)
    c = random.randint(-10, 10)
    d = random.randint(-10, 10)

    equation_str = f"{a}x^2 + {b}xy + {c} = {d}"

    expected_raw = (d - a * x**2 - c) / (b * x)
    expected_simplified = sp.simplify(expected_raw)

    rhs_step = sp.simplify(d - a * x**2 - c)
    step2 = f"{b}xy = {sp.sstr(rhs_step)}"
    step3 = f"y = {sp.sstr(expected_simplified)}"

    steps = [
        f"{a}x^2 + {b}xy + {c} = {d}",
        step2,
        step3
    ]

    return {
        "mode": "two",
        "equation_str": equation_str,
        "solve_for": "y",
        "expected_expr_str": sp.sstr(expected_simplified),
        "steps": steps
    }


def generate_problem(problem_type=None):
    if problem_type == "linear":
        return generate_linear()
    if problem_type == "quadratic":
        return generate_quadratic()
    if problem_type == "two_y":
        return generate_two_variable_solve_for_y()

    choice = random.choice(["linear", "quadratic"])
    if choice == "linear":
        return generate_linear()
    return generate_quadratic()
