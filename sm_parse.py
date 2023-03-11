#!/usr/bin/env python3
import os
import sys
from scenario import Scenario
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
    dir_list = os.listdir(sys.argv[1])
    files = [os.path.join(sys.argv[1], file) for file in dir_list]
    scenarios = list()
    for file in files:
        if file.endswith(".json"):
            print(file)
            scenarios.append(parse_file(file))
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
    table_t = np.array(table).transpose()
    return irr.fleiss_kappa(irr.aggregate_raters(table_t)[0], method='fleiss')


def prep_kappa(vectors):
    uc_name_kappa = 0
    uc_goal_kappa = 0
    uc_user_kappa = 0
    uc_system_kappa = 0
    uc_steps_kappa = 0
    uc_externalEntity_kappa = 0
    length = len(vectors)
    count = 0
    for i in range(length):

        if (len(vectors[i]['workers'])) == 3:
            count += 1
            uc_name_ratings = [vectors[i]['workers'][j]['annotations']['UC-Name'] for j in
                               range(len(vectors[i]['workers']))]
            uc_goal_ratings = [vectors[i]['workers'][j]['annotations']['UC-Goal'] for j in
                               range(len(vectors[i]['workers']))]
            uc_user_ratings = [vectors[i]['workers'][j]['annotations']['UC-User'] for j in
                               range(len(vectors[i]['workers']))]
            uc_system_ratings = [vectors[i]['workers'][j]['annotations']['UC-System'] for j in
                                 range(len(vectors[i]['workers']))]
            uc_steps_ratings = [
                vectors[i]['workers'][j]['annotations']['UC-step'] or vectors[i]['workers'][j]['annotations'][
                    'UC-DataPractice']
                for j in range(len(vectors[i]['workers']))]

            uc_name_kappa += calc_kappa(uc_name_ratings)
            uc_goal_kappa += calc_kappa(uc_goal_ratings)
            uc_user_kappa += calc_kappa(uc_user_ratings)
            uc_system_kappa += calc_kappa(uc_system_ratings)
            uc_steps_kappa += calc_kappa(uc_steps_ratings)

    diff = 50 - count
    kappa_counts = [uc_name_kappa, uc_goal_kappa, uc_user_kappa, uc_system_kappa, uc_steps_kappa]
    kappas = [(c + diff) / 50 for c in kappa_counts]

    return kappas


def example():
    scenarios = parse_args()
    print(len(scenarios))
    vectors = get_vectors(scenarios)
    print(len(vectors))
    print(vectors[0])
    print(prep_kappa(vectors))


if __name__ == '__main__':
    print_scenarios(parse_args())
