from Pyro4 import expose
import random
import time


class Solver:
    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers  # For compatibility with the parallel version
        print("Initialized.")

    def solve(self):
        print("Job Started")

        # Read the total number of iterations from the input file
        total_iterations = self.read_input()
        start_time = time.time()

        # Perform the sequential Monte Carlo simulation
        count_inside = Solver.calculate_pi(total_iterations)
        pi_estimate = 4.0 * count_inside / total_iterations
        elapsed_time = time.time() - start_time

        self.write_output(pi_estimate, elapsed_time, total_iterations)
        print("Finished in %.4f seconds." % elapsed_time)

    @staticmethod
    def calculate_pi(total_iterations):
        """
        Performs a sequential Monte Carlo simulation for the given number of iterations.
        Returns the count of points that fall inside the unit quarter circle.
        """
        count_inside = 0
        for _ in range(total_iterations):
            x = random.uniform(0, 1)
            y = random.uniform(0, 1)
            if x * x + y * y <= 1:
                count_inside += 1
        return count_inside

    @expose
    def calculate_pi_chunk(self, iterations):
        """
        Exposed method for remote calls. Works like calculate_pi but for a specified chunk of iterations.
        """
        return Solver.calculate_pi(iterations)

    def read_input(self):
        """
        Reads the input file. The first line of the file should contain an integer
        representing the total number of iterations for the simulation.
        """
        with open(self.input_file_name, 'r') as f:
            total_iterations = int(f.readline())
        return total_iterations

    def write_output(self, pi_estimate, elapsed_time, total_iterations):
        """
        Writes the output:
        - Execution time,
        - Total number of iterations,
        - Estimated value of Pi (with high precision, 10 decimal places).
        """
        with open(self.output_file_name, 'w') as f:
            output_text = "Finished in %.4f seconds." % elapsed_time
            f.write(output_text + '\n')
            f.write("Total iterations: %d\n" % total_iterations)
            f.write("Estimated Pi: %.10f\n" % pi_estimate)
