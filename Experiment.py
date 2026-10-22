import time, subprocess
from parsing import *
import config
from tqdm import tqdm
class Experiment:
    def __init__(self, parser, input_generator, iterations_per_test_case=10):
        self.parser = parser
        self.input_generator = input_generator
        self.input_strings = self.__get_input_strings()
        self.iterations_per_test_case = iterations_per_test_case
        self.experiment_result = []
        self.total_times_accepted = 0

    def __get_input_strings(self):
        return subprocess.run(self.input_generator,shell=True, capture_output=True,text=True).stdout.splitlines()

    def run_experiment(self):
            if config.verbose:
                print(f"Testing parser: {type(self.parser).__name__}")
                print(f"input generator: {self.input_generator}")
            for input in tqdm(self.input_strings):
                results = []
                times = []
                steps = 0
                times_accepted = 0
                if config.verbose:
                    print(f"\tInput string length: {len(input)}")
                for _ in range(self.iterations_per_test_case):
                    start_time = time.time()
                    results.append(self.parser.parse(input))
                    end_time = time.time()
                    times.append(end_time-start_time)
                    steps += self.parser.counter

                    times_accepted += 1 if results[-1] else 0

                for i in range(int(self.iterations_per_test_case * 0.2)):
                    times.pop(times.index(max(times,key=lambda x: abs(x-sum(times)/len(times)))))
                    times.pop(times.index(max(times,key=lambda x: abs(x-sum(times)/len(times)))))
                self.experiment_result.append([
                        len(input),
                        sum(times)/len(times), 
                        steps/self.iterations_per_test_case
                    ]
                )
                if config.verbose:
                    print(f"\t\tTimes accepted: {times_accepted}/{self.iterations_per_test_case}")
                    print(f"\t\tAvg_Time: {sum(times)/len(times):.4f}s")
                    print(f"\t\tAvg_Steps: {steps/self.iterations_per_test_case}")
                    if isinstance(self.parser, ErrorCorrection):
                        if results[-1]:
                            print(f"\t\tOriginal string: \t{input}")
                            print(f"\t\tCorrected string: \t{self.parser.get_corrected_string()}")
                            print(f"\t\tAmount of substitutions: {self.parser.get_amount_of_substitutions()},\tAmount of deletions: {self.parser.get_amount_of_deletions()}")
                        else:
                            print(f"\t\tOriginal string: {input}")
                            print(f"\t\tThere is no possible correction for this string.")

                self.total_times_accepted += times_accepted
            return self.experiment_result
