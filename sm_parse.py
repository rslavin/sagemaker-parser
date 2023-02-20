#!/usr/bin/env python3

from scenario import Scenario
from sys import argv

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


def example():
    scenarios = parse_args()
    # print_scenarios(scenarios)
    vectors = get_vectors(scenarios)
    print(vectors[0]['scenario'])
    print(vectors[0]['workers'][0]['annotations']['UC-System'])


if __name__ == '__main__':
    example()
