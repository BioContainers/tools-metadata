from ruamel.yaml import YAML
import requests
from difflib import SequenceMatcher

"""
This script takes the list of current annotations by name of the tool, etc: msgf and search in the list of all biotools a tool that has a similar name: similarity score > 0.95. The tool prints the recommended identifiers for all tools. 
"""

# Read the annotations file
yaml = YAML()
yaml_recipe = YAML(typ="rt")  # pylint: disable=invalid-name
with open('../annotations.yaml', 'r') as read_file:
    file_annotations = yaml.load(read_file)

tools = {}

# Create a list of all biotools
biotools_list = []
next_biotools_page = '?page=1'
while next_biotools_page is not None:
    url = 'https://bio.tools/api/tool/' + next_biotools_page + '&format=json'
    print(url)
    page = requests.get(url).json()
    biotools_list += page['list']
    next_biotools_page = page['next']


not_biotools = []
# check all the tools in the annotations file that do not contains biotools and try to find the corresponding biotools id by similarity scores.
for key in file_annotations:
    tool = file_annotations[key]

    if 'identifiers' not in tool:
        not_biotools.append(key)
    else:
        biotools = False
        for ids in tool['identifiers']:
            if 'biotools' in ids:
                biotools = True
        if not biotools:
            not_biotools.append(key)
for tool in not_biotools:
    for biotool in biotools_list:
        distance = SequenceMatcher(None, biotool['biotoolsCURIE'].replace('biotools:', ''), tool).ratio()
        if distance > 0.95:
            print('identifiers:\n      -   ' + biotool['biotoolsCURIE'])