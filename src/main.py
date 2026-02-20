from problem_generator import generate_problem
from numerical_methods import bisection, secant, newton


def main():
    while True:
        try:
            problem = generate_problem()
            break
        except ValueError:
            pass
    print("Solve the following equation:")
    print(problem["equation_str"])

    xl, xu = problem["bracket"]

    b = bisection(problem["f"], xl, xu)
    print("\nBisection:", b["converged"], b["root"], b["iterations"])

    s = secant(problem["f"], xl, xu)
    print("Secant:", s["converged"], s["root"], s["iterations"])

    n = newton(problem["f"], (xl + xu) / 2.0)
    print("Newton:", n["converged"], n["root"], n["iterations"])


if __name__ == "__main__":
    main()
