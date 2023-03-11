import json


class WorkerAnnotations:
    def __init__(self, scenario_content, worker_json):
        """
        Creates a WorkerAnnotation including a list of entities and a dictionary of label->vector pairs holding the
        character-based labels for the scenario.
        :param scenario_content: Scenario string
        :param worker_json: json object of worker annotations for the given scenario string
        """
        self.worker_id = worker_json['workerId']
        self.scenario = scenario_content
        self.entities = list()
        self.labels = dict()
        self.parse_annotations(scenario_content, worker_json['annotationData']['content'])

    def __str__(self):
        worker_str = f"Worker: {self.worker_id}\nAnnotations:\n"
        for entity in self.entities:
            worker_str += f'\t[{entity["label"]}]: "{entity["string"]}"\n'
        for label, chars in self.labels.items():
            worker_str += f'\t[{label}]: {str(chars)}\n'
        return worker_str

    def parse_annotations(self, scenario_content, annotation_content_json):
        """
        Generates the self.labels dictionary where keys are label types (e.g., "UC-System") and the values are lists of
        0s and 1s for each character in the scenario string. Also builds the self.entities list of dictionaries
        containing the labeled string and the label.
        :param scenario_content: Scenario string
        :param annotation_content_json: json object of annotation['content'] for an individual worker.
        :return:
        """
        entities = json.loads(annotation_content_json)['crowd-entity-annotation']['entities']
        entities.sort(key=lambda e: e['startOffset'])

        # initialize the label dictionaries with 0s
        self.labels['UC-System'] = [0] * len(scenario_content)
        self.labels['UC-Name'] = [0] * len(scenario_content)
        self.labels['UC-Goal'] = [0] * len(scenario_content)
        self.labels['UC-User'] = [0] * len(scenario_content)
        self.labels['UC-step'] = [0] * len(scenario_content)
        self.labels['UC-DataPractice'] = [0] * len(scenario_content)
        self.labels['UC-ExternalEntity'] = [0] * len(scenario_content)

        for entity in entities:
            # build self.entities for easy access to substrings
            self.entities.append({"string": scenario_content[entity['startOffset']:entity['endOffset']],
                                  "label": entity['label']})
            # fill in the 1s for each label
            # TODO update this to work for arbitrary labels
            self.labels[entity['label']] = [
                1 if entity['startOffset'] - 2 < i < entity['endOffset'] - 1 else 0 for (i, l) in
                enumerate(self.labels[entity['label']])]

    def compare_all(self):
        all_compare_str = ""
        for k in self.labels.keys():
            all_compare_str += self.compare(k)
        return all_compare_str

    def compare(self, label):
        """
        Prints the array of annotations for a given label along with the scenario to visualize the mappings
        :param label: label to print
        :return:
        """
        compare_str = label
        compare_str += "\n\t" + "".join(map(lambda x: str(x), self.labels[label]))
        compare_str += "\n\t" + self.scenario.strip('"') + "\n"
        return compare_str
