#!/usr/bin/env python3
"""
local_test.py

This script allows you to run the sequential Monte Carlo simulation locally to estimate Pi.
It creates an input file with the total number of iterations, runs the Solver, and prints the results.
"""

from no_parallel import Solver  # Assumes single.py is in the same directory as this file


def create_input_file(filename, iterations):
    """
    Creates an input file with the total number of iterations.

    Parameters:
        filename (str): The name of the input file.
        iterations (int): The total number of iterations for the simulation.
    """
    with open(filename, 'w') as f:
        f.write(str(iterations) + "\n")


def main():
    input_file = "input_large.txt"
    output_file = "output_large.txt"
    iterations = 100000000  # You can change this value to test with a different number of iterations

    # Create the input file containing the total number of iterations
    create_input_file(input_file, iterations)

    # Instantiate the Solver from the sequential version (single.py) and run the simulation
    solver = Solver(input_file_name=input_file, output_file_name=output_file)
    solver.solve()

    # Display the result by reading the output file
    print("Output:")
    with open(output_file, "r") as f:
         # Print the contents of the output file with the precision of 9
         result = f.read()
         print(result)


if __name__ == "__main__":
    main()
