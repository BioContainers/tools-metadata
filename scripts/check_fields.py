from metapub import PubMedFetcher
from metapub.convert import doi2pmid
from ruamel.yaml import YAML

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
    if 'license' not in tool:
        print(key)
    else:
        print (tool['license'])