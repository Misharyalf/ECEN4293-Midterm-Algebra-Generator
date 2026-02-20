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

    if f_xl == 0:
        return {"root": xl, "iterations": 0, "converged": True, "history": []}
    if f_xu == 0:
        return {"root": xu, "iterations": 0, "converged": True, "history": []}
    if f_xl * f_xu > 0:
        raise ValueError("Interval does not bracket a root: f(xl) and f(xu) have the same sign")

    history = []
    converged = False
    xm = None

    for i in range(1, max_iter + 1):
        xm = (xl + xu) / 2.0
        f_xm = f(xm)
        width = abs(xu - xl)

        history.append({
            "iter": i,
            "xl": xl,
            "xu": xu,
            "xm": xm,
            "f_xl": f_xl,
            "f_xu": f_xu,
            "f_xm": f_xm,
            "width": width
        })

        if width < tol or f_xm == 0:
            converged = True
            break

        if f_xl * f_xm < 0:
            xu = xm
            f_xu = f_xm
        else:
            xl = xm
            f_xl = f_xm

    return {"root": xm, "iterations": len(history), "converged": converged, "history": history}


def secant(f, x0, x1, tol=1e-6, max_iter=100):
    if not callable(f):
        raise TypeError("f must be a callable function")

    try:
        x0 = float(x0)
        x1 = float(x1)
        tol = float(tol)
        max_iter = int(max_iter)
    except (TypeError, ValueError) as err:
        raise TypeError("x0, x1, tol must be numbers and max_iter must be an int") from err

    if tol <= 0:
        raise ValueError("tol must be > 0")
    if max_iter <= 0:
        raise ValueError("max_iter must be > 0")
    if x0 == x1:
        raise ValueError("x0 and x1 must be different values")

    history = []
    converged = False

    f0 = f(x0)
    f1 = f(x1)

    if not (math.isfinite(f0) and math.isfinite(f1)):
        raise ValueError("f(x0) and f(x1) must be finite")

    for i in range(1, max_iter + 1):
        denom = (f1 - f0)
        if denom == 0:
            break

        x2 = x1 - f1 * (x1 - x0) / denom
        f2 = f(x2)

        if not math.isfinite(f2):
            break

        step = abs(x2 - x1)

        history.append({
            "iter": i,
            "x0": x0,
            "x1": x1,
            "x2": x2,
            "f_x0": f0,
            "f_x1": f1,
            "f_x2": f2,
            "step": step
        })

        if step < tol or f2 == 0:
            converged = True
            x1 = x2
            f1 = f2
            break

        x0, f0 = x1, f1
        x1, f1 = x2, f2

    return {"root": x1, "iterations": len(history), "converged": converged, "history": history}


def _numerical_derivative(f, x, h=1e-6):
    return (f(x + h) - f(x)) / h


def newton(f, x0, tol=1e-6, max_iter=100, df=None):
    if not callable(f):
        raise TypeError("f must be a callable function")

    if df is not None and (not callable(df)):
        raise TypeError("df must be a callable function or None")

    try:
        x0 = float(x0)
        tol = float(tol)
        max_iter = int(max_iter)
    except (TypeError, ValueError) as err:
        raise TypeError("x0, tol must be numbers and max_iter must be an int") from err

    if tol <= 0:
        raise ValueError("tol must be > 0")
    if max_iter <= 0:
        raise ValueError("max_iter must be > 0")

    history = []
    converged = False

    x = x0
    fx = f(x)

    if not math.isfinite(fx):
        raise ValueError("f(x0) must be finite")

    for i in range(1, max_iter + 1):
        if df is None:
            dfx = _numerical_derivative(f, x)
        else:
            dfx = df(x)

        if not math.isfinite(dfx) or dfx == 0:
            break

        x_new = x - fx / dfx
        fx_new = f(x_new)

        if not math.isfinite(fx_new):
            break

        step = abs(x_new - x)

        history.append({
            "iter": i,
            "x": x,
            "f_x": fx,
            "df_x": dfx,
            "x_new": x_new,
            "f_x_new": fx_new,
            "step": step
        })

        if step < tol or fx_new == 0:
            converged = True
            x = x_new
            fx = fx_new
            break

        x = x_new
        fx = fx_new

    return {"root": x, "iterations": len(history), "converged": converged, "history": history}
