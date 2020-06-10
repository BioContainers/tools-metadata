import os

from ruamel.yaml import YAML

yaml = YAML()
yaml_recipe = YAML(typ="rt")  # pylint: disable=invalid-name
with open('annotations.yaml.062020', 'r') as read_file:
    file_annotations = yaml.load(read_file)
tools = {}
for key in file_annotations:
    tool = file_annotations[key]
    if 'manually_check' not in tool:
        tool['manually_check'] = True
    tools[key] = tool

yaml.indent(mapping=4, sequence=6, offset=3)
with open('annotations.yaml', 'w') as outfile:
    yaml.dump(tools, outfile)