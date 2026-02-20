from problem_generator import generate_problem
from numerical_methods import bisection, secant, newton
from answer_checker import check_equivalent_y_in_terms_of_x


def read_choice(prompt, choices):
    while True:
        s = input(prompt).strip().lower()
        if s in choices:
            return s
        print("Invalid choice.")


def read_float(prompt):
    while True:
        s = input(prompt).strip()
        try:
            return float(s)
        except ValueError:
            print("Please enter a valid number.")


def format_history(result, method):
    h = result.get("history", [])
    if not h:
        return f"root={result.get('root')}, iterations={result.get('iterations')}, converged={result.get('converged')}"

    lines = []
    if method == "bisection":
        lines.append("iter\txl\txu\txm\tf(xm)\twidth")
        for row in h:
            lines.append(
                f'{row["iter"]}\t{row["xl"]:.6f}\t{row["xu"]:.6f}\t{row["xm"]:.6f}\t{row["f_xm"]:.6f}\t{row["width"]:.6f}'
            )
    elif method == "secant":
        lines.append("iter\tx0\tx1\tx2\tf(x2)\tstep")
        for row in h:
            lines.append(
                f'{row["iter"]}\t{row["x0"]:.6f}\t{row["x1"]:.6f}\t{row["x2"]:.6f}\t{row["f_x2"]:.6f}\t{row["step"]:.6f}'
            )
    else:
        lines.append("iter\tx\tf(x)\tdf(x)\tx_new\tstep")
        for row in h:
            lines.append(
                f'{row["iter"]}\t{row["x"]:.6f}\t{row["f_x"]:.6f}\t{row["df_x"]:.6f}\t{row["x_new"]:.6f}\t{row["step"]:.6f}'
            )

    return "\n".join(lines)



def solve_single(problem, method):
    f = problem["f"]
    xl, xu = problem["bracket"]

    if xl == xu:
        return {"root": xl, "iterations": 0, "converged": True, "history": []}

    if method == "bisection":
        return bisection(f, xl, xu)

    if method == "secant":
        return secant(f, xl, xu)

    return newton(f, (xl + xu) / 2.0)



def run_single_variable():
    abs_tol = 1e-2
    rel_tol = 1e-2

    print("\nSingle-variable mode")
    print("Enter numeric x")
    print("Answer tolerance:", abs_tol, "(abs),", rel_tol, "(rel)\n")

    while True:
        while True:
            try:
                problem = generate_problem()
                break
            except ValueError:
                pass

        print("Solve:", problem["equation_str"])

        print("Choose method:")
        print(" 1=bisection")
        print(" 2=secant")
        print(" 3=newton\n")

        m = read_choice("Enter choice: ", {"1", "2", "3"})
        method = {"1": "bisection", "2": "secant", "3": "newton"}[m]

        result = solve_single(problem, method)

        if not result["converged"]:
            print("Solver did not converge. New problem.\n")
            continue

        correct_root = result["root"]

        while True:
            user_x = read_float("Enter your answer for x: ")
            if abs(user_x - correct_root) <= max(abs_tol, rel_tol * abs(correct_root)):
                print("Correct!\n")
                break

            print("Not correct.")
            show = read_choice("Show step-by-step solution? (y/n): ", {"y", "n"})
            if show == "y":
                print(format_history(result, method))
                xl, xu = problem["bracket"]
                print("Bracket:", xl, xu)

            print()

        cont = read_choice("New problem? (y/n): ", {"y", "n"})
        print()
        if cont == "n":
            break


def run_two_variable():
    print("\nTwo-variable mode")
    print("Solve for y in terms of x")
    print("Enter an expression for y using x, example: (3*x**2-1)/(2*x)\n")

    while True:
        problem = generate_problem("two_y")
        print("Solve for y:", problem["equation_str"])

        expected = problem["expected_expr_str"]

        while True:
            user_expr = input("Enter your expression for y: ").strip()
            ok = check_equivalent_y_in_terms_of_x(user_expr, expected)
            if ok:
                print("Correct!\n")
                break

            print("Not correct.")
            show = read_choice("Show step-by-step solution? (y/n): ", {"y", "n"})
            if show == "y":
                for s in problem["steps"]:
                    print(s)
            print()

        cont = read_choice("New problem? (y/n): ", {"y", "n"})
        print()
        if cont == "n":
            break


def main():
    print("Algebra Practice Program")
    while True:
        print("\nChoose mode:")
        print(" 1=single-variable")
        print(" 2=two-variable")
        print(" q=quit\n")

        mode = read_choice("Enter choice: ", {"1", "2", "q"})
        if mode == "1":
            run_single_variable()
        elif mode == "2":
            run_two_variable()
        else:
            break


if __name__ == "__main__":
    main()
