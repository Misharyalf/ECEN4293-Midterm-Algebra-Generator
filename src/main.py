"""
Main execution file for Algebra Homework Generator.
"""

from problem_generator import generate_problem


def main():
    problem = generate_problem()

    print("Solve the following equation:")
    print(problem["equation_str"])


if __name__ == "__main__":
    main()
