from metapub import PubMedFetcher
from metapub.convert import doi2pmid
from ruamel.yaml import YAML
import requests
from difflib import SequenceMatcher

"""
The following script will read doi accessions in the identifiers section of the tool and find the pubmed accession of corresponding to it. 
Finally, if the pubmed accession is found, the script will look for mesh keywords associated with the publications and added to the tool_tags. 
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
        not_biotools.append(key)
    else:
        dois = False
        for ids in tool['identifiers']:
            if 'doi' in ids:
                dois = True
        if not dois:
            not_biotools.append(key)

for tool in not_biotools:
    print(tool)