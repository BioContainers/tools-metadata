import requests
from ruamel.yaml import YAML
top_words = ['Algorithms', 'Software']

"""
The following script will read doi accessions in the identifiers section of the tool and find the pubmed accession of corresponding to it. 
Finally, if the pubmed accession is found, the script will look for mesh keywords associated with the publications and added to the tool_tags. 
"""

yaml = YAML()
yaml_recipe = YAML(typ="rt")  # pylint: disable=invalid-name
with open('../annotations.yaml', 'r') as read_file:
    file_annotations = yaml.load(read_file)

tools = {}

for key in file_annotations:
    tool = file_annotations[key]
    if 'keywords' in tool:
        result_keywords = tool['keywords']
    else:
        result_keywords = []
    if 'identifiers' in tool:
        identifiers = tool['identifiers']
        for identifier in identifiers:
            try:
                if 'biotools' in identifier:
                    biotool_accession = identifier.replace('biotools:', '')
                    url = 'https://bio.tools/api/tool/' + biotool_accession + '?format=json'
                    biotool = requests.get(url).json()
                    if 'topic' in biotool:
                        for topic in biotool['topic']:
                            result_keywords.append(topic['term'])
            except Exception as e:
                print('Error biotool --' + identifier)
    result_keywords = list(dict.fromkeys(result_keywords))
    tool['keywords'] = result_keywords
    tools[key] = tool

yaml.indent(mapping=4, sequence=6, offset=2)
with open('missing_annotations.yaml', 'w') as outfile:
    yaml.dump(tools, outfile)