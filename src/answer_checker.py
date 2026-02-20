import sympy as sp


def check_equivalent_y_in_terms_of_x(user_expr_str, expected_expr_str):
    x = sp.Symbol("x")
    try:
        user_expr = sp.sympify(user_expr_str, locals={"x": x})
        expected_expr = sp.sympify(expected_expr_str, locals={"x": x})
    except Exception:
        return False

    try:
        diff = sp.simplify(user_expr - expected_expr)
        return diff == 0
    except Exception:
        return False
