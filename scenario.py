import json
from workerannotations import WorkerAnnotations


class Scenario:
    def __init__(self, json_str):
        """
        Creates a Scenario object from a json string. The scenario includes a list of workers and the content (i.e.,
        scenario string).
        :param json_str: raw json string
        """
        self.workers = list()
        self.content = json.loads(json_str)[0]['dataObject']['content']
        for a in json.loads(json_str)[0]['annotations']:
            self.workers.append(WorkerAnnotations(self.content, a))

    def __str__(self):
        scenario_str = f"Scenario: {self.content}\n\n"
        for worker in self.workers:
            scenario_str += worker.__str__()
        return scenario_str

    def get_annotations(self):
        """
        Creates a dictionary with keys 'scenario' and 'workers' where 'scenario' is the scenario string as a vector of
        characters and 'workers' is a list of worker dictionaries. Each worker dictionary has keys 'id' and
        'annotations' where 'id' is the worker id and 'annotations' is a dictionary of labels with keys corresponding
        to each label and values as a list of 0s and 1s mapping to character positions in the scenario.
        :return:
        """
        annotations = dict()
        annotations['scenario'] = [*self.content.strip('"')]
        annotations['workers'] = list()
        for worker in self.workers:
            annotations['workers'].append({'id': worker.worker_id, 'annotations': worker.labels})
        return annotations
