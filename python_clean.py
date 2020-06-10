import os

import requests
from ruamel.yaml import YAML

yaml = YAML()
yaml_recipe = YAML(typ="rt")  # pylint: disable=invalid-name
with open('annotations.yaml', 'r') as read_file:
    file_annotations = yaml.load(read_file)
tools = {}
for key in file_annotations:
    tool = file_annotations[key]
    if tool['manually_check'] == False or (tool["home_url"] is not None and "{{ bioc }}" in tool['home_url']) or (tool['home_url'] is None or len(tool['home_url'])==0):
        url = "https://api.anaconda.org/package/bioconda/" + key
        resp = requests.get(url)
        if resp.status_code == 200:
            # This means something went wrong.
            todo_item = resp.json()
            tool['description'] = todo_item['summary']
            tool['license'] = todo_item['license']
            tool['home_url'] = todo_item['home']
            print("Log check -- " + key)
    print(key)
    if tool['home_url'] is None or len(tool['home_url'].strip()) == 0:
        tool['manually_check'] = False
    tools[key] = tool



yaml.indent(mapping=4, sequence=6, offset=3)
with open('missing_annotations.yaml', 'w') as outfile:
    yaml.dump(tools, outfile)