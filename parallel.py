from Pyro4 import expose
import random
import time


class Solver:
    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers
        print("Initialized.")

    def solve(self):
        print("Job Started")
        print("Workers: %d" % len(self.workers))

        # Read the total number of iterations from the input file
        total_iterations = self.read_input()

        # Divide iterations evenly among workers
        num_workers = len(self.workers)
        iterations_per_worker = total_iterations // num_workers
        iterations_chunks = []
        for i in range(num_workers):
            if i == num_workers - 1:
                # Last worker receives any remaining iterations
                chunk_iterations = iterations_per_worker + (total_iterations % num_workers)
            else:
                chunk_iterations = iterations_per_worker
            iterations_chunks.append(chunk_iterations)

        mapped = []
        start_time = time.time()
        # Distribute the computation across workers
        for i in range(num_workers):
            mapped.append(
                self.workers[i].calculate_pi_chunk(iterations_chunks[i])
            )

        # Sum the results from all workers
        total_inside = 0
        for result in mapped:
            total_inside += result.value

        # Estimate Pi using the formula:
        # pi = 4 * (points inside quarter circle) / total iterations
        pi_estimate = 4.0 * total_inside / total_iterations
        elapsed_time = time.time() - start_time

        print("Finished in %.4f seconds." % elapsed_time)
        self.write_output(pi_estimate, elapsed_time, total_iterations)

    @expose
    def calculate_pi_chunk(self, iterations):
        """
        Performs the Monte Carlo simulation for a given number of iterations.
        Randomly generates points and counts how many fall inside the unit quarter circle.
        """
        count_inside = 0
        for _ in range(iterations):
            x = random.uniform(0, 1)
            y = random.uniform(0, 1)
            if x * x + y * y <= 1:
                count_inside += 1
        return count_inside

    def read_input(self):
        """
        Reads the input file. The file should contain an integer in the first line,
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
            output_text = "Finished in %.4f seconds using %d workers" % (elapsed_time, len(self.workers))
            f.write(output_text + '\n')
            f.write("Total iterations: %d\n" % total_iterations)
            f.write("Estimated Pi: %.10f\n" % pi_estimate)
