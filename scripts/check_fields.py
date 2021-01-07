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

# check biotools accessions
biotools_list = []
next_biotools_page = '?page=1'
while next_biotools_page is not None:
    print('getting page %s' % next_biotools_page)
    url = 'https://bio.tools/api/tool/' + next_biotools_page + '&format=json'
    page = requests.get(url).json()
    biotools_list += page['list']
    next_biotools_page = page['next']


not_biotools = []
# check bio.tools
for key in file_annotations:
    tool = file_annotations[key]

    if 'identifiers' not in tool:
        print(key)
        not_biotools.append(key)
    else:
        biotools = False
        for ids in tool['identifiers']:
            if 'biotools' in ids:
                biotools = True
        if not biotools:
            print(key)
            not_biotools.append(key)
for tool in not_biotools:
    for biotool in biotools_list:
        distance = SequenceMatcher(None, biotool['biotoolsCURIE'].replace('biotools:', ''), tool).ratio()
        if distance > 0.95:
            #print(biotool['biotoolsCURIE'].replace('biotools:', '') + "\t" + tool + "\t: " + str(distance))
            print('identifiers:\n   t-  ' + biotool['biotoolsCURIE'])