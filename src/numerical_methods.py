"""
Numerical Methods Module
Root-finding methods consistent with course notes.
"""

import math


def bisection(f, xl, xu, tol=1e-6, max_iter=100):
    

    if not callable(f):
        raise TypeError("f must be a callable function")

    try:
        xl = float(xl)
        xu = float(xu)
        tol = float(tol)
        max_iter = int(max_iter)
    except (TypeError, ValueError) as err:
        raise TypeError("xl, xu, tol must be numbers and max_iter must be an int") from err

    if tol <= 0:
        raise ValueError("tol must be > 0")
    if max_iter <= 0:
        raise ValueError("max_iter must be > 0")
    if xl == xu:
        raise ValueError("xl and xu must be different values")
    if xl > xu:
        xl, xu = xu, xl

    f_xl = f(xl)
    f_xu = f(xu)

    if not (math.isfinite(f_xl) and math.isfinite(f_xu)):
        raise ValueError("f(xl) and f(xu) must be finite")

    # Must bracket a root
    if f_xl == 0:
        return {
            "root": xl,
            "iterations": 0,
            "converged": True,
            "history": []
        }
    if f_xu == 0:
        return {
            "root": xu,
            "iterations": 0,
            "converged": True,
            "history": []
        }
    if f_xl * f_xu > 0:
        raise ValueError("Interval does not bracket a root: f(xl) and f(xu) have the same sign")

    history = []
    converged = False
    xm = None

    for i in range(1, max_iter + 1):
        xm = (xl + xu) / 2.0
        f_xm = f(xm)

        interval_width = abs(xu - xl)

        # Save iteration row for step-by-step guide
        history.append({
            "iter": i,
            "xl": xl,
            "xu": xu,
            "xm": xm,
            "f_xl": f_xl,
            "f_xu": f_xu,
            "f_xm": f_xm,
            "width": interval_width
        })

        # Stopping conditions
        if interval_width < tol or f_xm == 0:
            converged = True
            break

        # Decide which half contains the root
        if f_xl * f_xm < 0:
            xu = xm
            f_xu = f_xm
        else:
            xl = xm
            f_xl = f_xm

    return {
        "root": xm,
        "iterations": len(history),
        "converged": converged,
        "history": history
    }
