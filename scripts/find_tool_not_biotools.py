
from ruamel.yaml import YAML
import requests

"""
This script print all the tools that do not have a corresponding biotools accession or doi.   
"""

yaml = YAML()
yaml_recipe = YAML(typ="rt")  # pylint: disable=invalid-name
with open('../annotations.yaml', 'r') as read_file:
    file_annotations = yaml.load(read_file)

tools = {}
not_biotools = []


def search_tool(key):
    url = 'https://www.ebi.ac.uk/europepmc/webservices/rest/search?query="'+key+'"&format=json&pageSize=1000'
    page = requests.get(url).json()
    if page['hitCount'] == 1 and 'resultList' in page:
        for publication in page['resultList']['result']:
            try:
                print(key + ' ---- ' + publication['title'] + ' --- ' + publication['doi'])
            except Exception as e:
                print('Error doi --' + publication['title'])
    print('----------------------------------------------')


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
            search_tool(key)
        if not biotools:
            not_biotools.append(key + ' -- not biotools')

for tool in not_biotools:
    print(tool)
