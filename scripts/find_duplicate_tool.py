from difflib import SequenceMatcher

from ruamel.yaml import YAML

"""
This script try to find duplicated tools in the annotation file
"""

yaml = YAML()
yaml_recipe = YAML(typ="rt")  # pylint: disable=invalid-name
with open('../annotations.yaml', 'r') as read_file:
    file_annotations = yaml.load(read_file)

tools = file_annotations.values()
import itertools


def get_biotools(a):
    biotool = None
    if 'identifiers' in a:
        for identifier in a['identifiers']:
            if 'biotool' in identifier:
                biotool = identifier
    return biotool


def compare(a, b):
    biotool_a = get_biotools(a)
    biotool_b = get_biotools(b)
    if biotool_a is not None and biotool_b is not None:
        return biotool_a == biotool_b
    return SequenceMatcher(None, a['name'].replace('biotools:', ''), b['name'].replace('biotools:', '')).ratio() > 0.95


for a, b in itertools.combinations(tools, 2):
    if 'name' not in a or 'name' not in b:
        print("Error")
    if compare(a, b):
        print('Tools: ' + a['name'] + " and " + b['name'] + " equal")
