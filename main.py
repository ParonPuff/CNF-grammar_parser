import csv
import sys, argparse, json
from parsing import *
from Experiment import Experiment
from CnfGrammar import CnfGrammar
from LinearGrammar import LinearGrammar
import config
import os

def read_json_file(json_file):
    all_experiments = []
    experiment_labels = []
    dirname = os.path.dirname(json_file)
    with(open(json_file,'r')) as file:
        data = json.load(file)
        for key,grammar in data.items():
            experiment_labels.append(key)

            grammar_object = None
            try:
                grammar_object = CnfGrammar.from_file(os.path.join(dirname,grammar['grammar_path']))
            except:
                grammar_object = LinearGrammar(os.path.join(dirname,grammar['grammar_path']))

            parser_implementation = globals()[grammar['algorithm']](grammar_object)#[obj(grammar_obejct) for obj in Parser.__subclasses__()]#[naive, bu, td]
            all_experiments.append(Experiment(parser_implementation,os.path.join(dirname,grammar['test_cases']),10))
        file.close()
    return all_experiments, experiment_labels

def main(argv) -> int:
    argument_parser = argparse.ArgumentParser(
            prog = "CykTester",
            description = "Tests cyk algorithims"
            )

    argument_parser.add_argument("json_file")
    argument_parser.add_argument("-l", "--log", action="store_true",
            help="Log the results of the experiment to a file"
            )
    argument_parser.add_argument("-v", "--verbose", action="store_true",
            help="Print the results of the experiment to the console"
            )
    parsed_args = argument_parser.parse_args(argv)
    config.verbose = parsed_args.verbose

    all_experiments, experiment_labels = read_json_file(parsed_args.json_file)
    working_directory = os.path.dirname(__file__)
    for idx,experiment in enumerate(all_experiments):
        print(f"**********Running {experiment_labels[idx]}**********")
        data = []
        data.append(["length","avg_time", "avg_steps"])
        for elements in experiment.run_experiment():
            data.append(elements)
        if parsed_args.log:
            with open(os.path.join(working_directory,f'./data/{experiment_labels[idx]}.csv'),'w+',newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                writer.writerows(data)
            csvfile.close()

    print("All experiments completed without error.")
    if parsed_args.log:
        print("Results are saved in the data folder.")

    accepted = []
    for experiment in all_experiments:
        accepted.append(str(experiment.total_times_accepted) + "/" + str(experiment.iterations_per_test_case*len(experiment.input_strings)))
    for name, acc in zip(experiment_labels, accepted):
        print(f"{name}: {acc}")
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
