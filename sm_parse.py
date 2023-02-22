#!/usr/bin/env python3

from scenario import Scenario
from sys import argv
import numpy as np
from statsmodels.stats import inter_rater as irr

def parse_file(file_path):
    """
    Parses a scenario from json string in one file.
    :param file_path: path to file
    :return: Scenario object
    """
    try:
        with open(file_path) as f:
            return Scenario(f.read())
    except FileNotFoundError:
        print(f'ERROR: File not found: {file_path}')
    return None

def parse_args():
    """
    Parses scenarios from files given as command line arguments. Expects one string per file.
    :return: list of Scenarios
    """
    scenarios = list()
    for arg in argv[1:]:
        scenarios.append(parse_file(arg))
    return scenarios


def print_scenarios(scenarios):
    """
    Prints scenarios in a neat way to visualize the label alignments
    :param scenarios:
    """
    for scenario in scenarios:
        print(f"Scenario: {scenario.content}")
        for worker in scenario.workers:
            print(f"\nWorker: {worker.worker_id}")
            print(worker.compare_all())


def get_vectors(scenarios):
    """
    Produces a list of dictionaries with keys 'worker' and 'scenario'. Each worker is a list of dictionaries with keys
    'id' and 'annotations' where id is the worker id and annotations is a list of annotations. Each annotation is a
    dictionary of labels pointing to lists of 0s and 1s corresponding to the characters in the scenario.
    :param scenarios:
    :return:
    """
    vectors = list()
    for scenario in scenarios:
        vectors.append(scenario.get_annotations())
    return vectors


def calc_kappa(table):
    """

    :param table: a table with three rows and n columns. Each row is associated with one worker.
    n is the number of characters in a scenario.
    :return: fleiss kappa, inter-rater agreement between three workers
    https://stackoverflow.com/questions/56481245/inter-rater-reliability-calculation-for-multi-raters-data
    """
    tableT = np.array(table).transpose()
    return irr.fleiss_kappa(irr.aggregate_raters(tableT)[0], method='fleiss')

def prep_kappa(vectors):
    uc_name_kappa = 0
    uc_goal_kappa = 0
    uc_user_kappa = 0
    uc_system_kappa = 0
    uc_steps_kappa = 0
    length = len(vectors)

    for i in range(length):
        uc_name_ratings = [v['workers'][j]['annotations']['UC-Name'] for v in vectors for j in range(len(v['workers']))]
        uc_goal_ratings = [v['workers'][j]['annotations']['UC-Goal'] for v in vectors for j in range(len(v['workers']))]
        uc_user_ratings = [v['workers'][j]['annotations']['UC-User'] for v in vectors for j in range(len(v['workers']))]
        uc_system_ratings = [v['workers'][j]['annotations']['UC-System'] for v in vectors for j in range(len(v['workers']))]
        uc_steps_ratings = [v['workers'][j]['annotations']['UC-step'] or v['workers'][j]['annotations']['UC-DataPractice'] for v in vectors for j in range(len(v['workers']))]

        uc_name_kappa += calc_kappa(uc_name_ratings)
        uc_goal_kappa += calc_kappa(uc_goal_ratings)
        uc_user_kappa += calc_kappa(uc_user_ratings)
        uc_system_kappa += calc_kappa(uc_system_ratings)
        uc_steps_kappa += calc_kappa(uc_steps_ratings)

    return [uc_name_kappa/length, uc_goal_kappa/length, uc_user_kappa/length, uc_system_kappa/length, uc_steps_kappa/length];


def example():
    scenarios = parse_args()
    # print_scenarios(scenarios)
    vectors = get_vectors(scenarios)
    print(prep_kappa(vectors))


if __name__ == '__main__':
    example()
