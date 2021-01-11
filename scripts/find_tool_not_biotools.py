
from ruamel.yaml import YAML

"""
This script print all the tools that do not have a corresponding biotools accession or doi.   
"""

yaml = YAML()
yaml_recipe = YAML(typ="rt")  # pylint: disable=invalid-name
with open('../annotations.yaml', 'r') as read_file:
    file_annotations = yaml.load(read_file)

tools = {}
not_biotools = []
for key in file_annotations:
    tool = file_annotations[key]

    if 'identifiers' not in tool:
        not_biotools.append(key + ' -- not biotools, dois')
    else:
        dois = False
        biotools = False
        for ids in tool['identifiers']:
            if 'doi' in ids:
                dois = True
            if 'biotools' in ids:
                biotools = True
        if not dois:
            not_biotools.append(key + ' -- not dois')
        if not biotools:
            not_biotools.append(key + ' -- not biotools')

for tool in not_biotools:
    print(tool)