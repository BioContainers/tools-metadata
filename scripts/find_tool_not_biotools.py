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
    count = 0
    url = 'https://www.ebi.ac.uk/europepmc/webservices/rest/search?query="' + key + '"&format=json&pageSize=1000'
    page = requests.get(url).json()
    if 'resultList' in page:
        for publication in page['resultList']['result']:
            try:
                common_name = key + ":"
                # if common_name in publication['title'].lower() and (
                #         'nmeth.' in publication['doi'] or 'bioinformatics' in publication['doi'] or 'nar\/' in publication['doi'] or 'gigascience' in publication['doi'] or 'nbt.' in publication['doi']):
                #     print(key + ' ---- ' + publication['title'] + ' --- ' + publication['doi'])
                if common_name in publication['title'].lower():
                    print(key + ' ---- ' + publication['title'] + ' --- ' + '  -' + '   doi:' + publication['doi'])
            except Exception:
                # print('Error doi --' + key)
               count = count + 1
    # print('----------------------------------------------')

count = 0
for key in file_annotations:
    tool = file_annotations[key]

    if 'no_doi' not in tool and ('identifiers' not in tool or len(tool['identifiers']) == 0):
           not_biotools.append(key)
           print(key + "\t" + tool['home_url'] + "\t")
           count = count + 1
    # else:
    #     if not any("doi" in word for word in tool['identifiers']):
    #         not_biotools.append(key)
print(str(count))
for tool in not_biotools:

    if 'bioconductor-' in tool:
        tool = tool.replace("bioconductor-", "");
    if 'r-' in tool:
        tool = tool.replace("r-", "");

    search_tool(tool)
    count = 0
