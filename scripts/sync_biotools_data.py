import json
import os
import urllib

from bioconda_utils import recipe
from ruamel.yaml import YAML

"""
This script read the metadata from bioconda repo and annotate the metadata from the recipes in the tools 
"""
yaml = YAML()
yaml_recipe = YAML(typ="rt")  # pylint: disable=invalid-name
with open('../annotations.yaml', 'r') as read_file:
    file_annotations = yaml.load(read_file)

recipes_path = "/Users/yperez/IdeaProjects/github-repo/biodocker/content/data/{}/{}.bioschemas.jsonld"
folder_path = "/Users/yperez/IdeaProjects/github-repo/biodocker/content/data/{}/{}.biotools.json"
debian_path = "/Users/yperez/IdeaProjects/github-repo/biodocker/content/data/{}/{}.debian.yaml"
tools = {}

### Annotate bioconductor package
for key in file_annotations:
    tool = file_annotations[key]
    path_jsonld = recipes_path.format(key, key)
    path_biotools = folder_path.format(key, key)
    path_debian = debian_path.format(key,key)

    # folder = folder_path.format(key)

    identifiers = []
    if 'identifiers' in tool:
        identifiers = tool['identifiers']

    # if not any("doi" in word for word in identifiers) and os.path.isdir(folder):
    #     print(folder)

    if not any("doi" in word for word in identifiers) and os.path.isfile(path_jsonld):
        with open(path_jsonld) as f:
            data = json.load(f)
            if '@graph' in data:
                for entity in data['@graph']:
                    if 'doi' in entity['@id']:
                        identifiers.append(entity['@id'].replace('https://doi.org/',''))
    else:
        if not any("doi" in word for word in identifiers) and os.path.isfile(path_biotools):
            with open(path_biotools) as f:
                data = json.load(f)
                if 'publication' in data:
                    for publication in data['publication']:
                        if 'doi' in publication:
                            identifiers.append(publication['doi'])
        if not any("doi" in word for word in identifiers) and os.path.isfile(path_debian):
            with open(path_debian) as f:
                data = yaml.load(f)
                if 'publication' in data:
                    for publication in data['publication']:
                        if 'doi' in publication:
                            identifiers.append(publication['doi'])

    identifiers = list(dict.fromkeys(identifiers))
    tool['identifiers'] = identifiers
    tools[key] = tool

# writing missing

yaml.indent(mapping=4, sequence=6, offset=2)
with open('missing_annotations.yaml', 'w') as outfile:
    yaml.dump(tools, outfile)