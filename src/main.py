"""
Main execution file for Algebra Homework Generator.
"""

from problem_generator import generate_problem
from numerical_methods import bisection


def main():
    problem = generate_problem()
    print("Solve the following equation:")
    print(problem["equation_str"])

   
    result = bisection(problem["f"], xl=-100, xu=100)

    print("\nBisection Result")
    print("Converged:", result["converged"])
    print("Root:", result["root"])
    print("Iterations:", result["iterations"])


if __name__ == "__main__":
    main()
