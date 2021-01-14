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
    url = 'https://www.ebi.ac.uk/europepmc/webservices/rest/search?query="' + key + '"&format=json&pageSize=1000'
    page = requests.get(url).json()
    if 'resultList' in page:
        for publication in page['resultList']['result']:
            try:
                common_name = key + ":"
                if common_name in publication['title'].lower() and (
                        'nmeth.' in publication['doi'] or 'bioinformatics' in publication['doi'] or 'nar\/' in publication['doi'] or 'gigascience' in publication['doi'] or 'nbt.' in publication['doi']):
                    print(key + ' ---- ' + publication['title'] + ' --- ' + publication['doi'])
            except Exception:
                print('Error doi --' + key)
    # print('----------------------------------------------')


for key in file_annotations:
    tool = file_annotations[key]

    if 'identifiers' not in tool:
        not_biotools.append(key)
    else:
        if not any("doi" in word for word in tool['identifiers']):
            not_biotools.append(key)

for tool in not_biotools:
    if 'bioconductor-' in tool:
        search_tool(tool.replace("bioconductor-", ""))
    else:
        search_tool(tool)
