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
    result_identifiers = []
    if 'identifiers' in tool:
        identifiers = tool['identifiers']
        for identifier in identifiers:
            result_identifiers.append(identifier)
            try:
                if 'biotools' in identifier:
                    biotool_accession = identifier.replace('biotools:', '')
                    url = 'https://bio.tools/api/tool/' + biotool_accession + '?format=json'
                    biotool = requests.get(url).json()
                    if 'publication' in biotool:
                        for publication in biotool['publication']:
                            add_pub = False
                            if 'doi' in publication and publication['doi'] is not None:
                                result_identifiers.append('doi:' + publication['doi'])
                                add_pub = True
                            else:
                                if 'pmid' in publication and publication['pmid'] is not None:
                                    url='https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?tool=my_tool&email=my_email@example.com&ids='+publication['pmid'] + '&format=json';
                                    doi_info = requests.get(url).json()
                                    if 'records' in doi_info:
                                        if 'doi' in doi_info['records'][0] and 'status' not in doi_info['records'][0]:
                                            result_identifiers.append('doi:' + doi_info['records'][0]['doi'])
                                        else:
                                            result_identifiers.append('pmid:' + publication['pmid'])
                                    else:
                                        result_identifiers.append('pmid:' + publication['pmid'])
                                    add_pub = True
                            if not add_pub:
                                raise Exception('Publication not found: ' + publication['metadata']['title'])
            except Exception as e:
                print('Error biotool --' + identifier)
        result_identifiers = list(dict.fromkeys(result_identifiers))
        tool['identifiers'] = result_identifiers
    tools[key] = tool

yaml.indent(mapping=4, sequence=6, offset=2)
with open('missing_annotations.yaml', 'w') as outfile:
    yaml.dump(tools, outfile)