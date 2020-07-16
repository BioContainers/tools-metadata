from ruamel.yaml import YAML
from urlextract import URLExtract
import urllib

import re
from collections import OrderedDict

"""
This script takes url with html and try to detect links to doi files (publications). The input of the script is the ../annotations.yaml. 
For each tool in the annotatios.yaml, the scripts read the home_url for each tool, get the html and try to detect doi urls. 

The output of the script will will go to a new file missing_annotations.yaml. The curator needs to finally accept the new changes. 
"""

# DOI regular expressions
doiurl_re = re.compile("doi:\s?(10\.[a-z0-9\-._:;()/<>]+)", re.U)  # Matches doi:(10. ... )
doispace_re = re.compile("doi\s?(10\.[a-z0-9\-._:;()/<>]+)", re.U)  # Matches doi (10. ... )
dx_re = re.compile("dx.doi.org/(10\.[a-z0-9\-._:;()/<>]+)", re.U)  # Matches dx.doi.org/(10. ...)
doi_re = re.compile("(?:\s|^)(10\.[0-9.]+/[a-z0-9\-._:;()/<>]+)", re.U)  # Mathces (10. ... )


def doi_from_text(text):
    """
    find a doi url in a free-text
    :param text:  text
    :return:  doi
    """
    doi_numbers = []
    for line in text.splitlines():
        line = line.lower()
        if 'doi' in line:
            for d in doiurl_re.findall(line):
                doi_numbers.append(clean_doi(d))
            for d in doispace_re.findall(line):
                doi_numbers.append(clean_doi(d))
            for d in dx_re.findall(line):
                doi_numbers.append(clean_doi(d))
        elif "10." in line:
            for d in doi_re.findall(line):
                doi_numbers.append(clean_doi(d))

    doi_numbers = list(OrderedDict.fromkeys(doi_numbers))
    return doi_numbers


def clean_doi(d):
    """
    Cleans the DOI of extranious but valid characters at the end.  If my regex fu were
    better I bet I wouldn't need this method.
    Removes a trailing '.' and removes a trailing ')' if '(' and ')' counts don't match
    """
    if d[-1] == '.': d = d[:-1]  # end of a sentence
    if d[-1] == ')' and d.count('(') != d.count(')'): d = d[:-1]  # in () not seperated by a space
    if d[-1] == ';': d = d[:-1]  # poorly formated list
    if d[-4:] == '</a>': d = d[:-4]  # an anchor tag
    return d


def retrieve_doi(url):
    dois = []
    with urllib.request.urlopen(url) as url:
        s = url.read().decode('utf-8')
        text = s.replace(' ', '').replace('=', '')
        extractor = URLExtract()
        urls = extractor.find_urls(text)
        dois = find_doi_string_regex(urls)
    return dois


def find_doi_string_regex(urls):
    dois = []
    for url in urls:
        doi = doi_from_text(url)
        if doi is not None and len(doi) > 0:
            dois = dois + doi
    return dois


yaml = YAML()
yaml_recipe = YAML(typ="rt")  # pylint: disable=invalid-name
with open('../annotations.yaml', 'r') as read_file:
    file_annotations = yaml.load(read_file)

tools = {}

### Annotate bioconductor package
for key in file_annotations:
    tool = file_annotations[key]
    url = tool['home_url']
    try:
        dois = retrieve_doi(url)
        print(dois)
        if len(dois) > 0:
            identifiers = []
            if 'identifiers' in tool:
                identifiers = tools['identifiers']
            for doi in dois:
                identifiers.append('doi:' + doi)
            identifiers = list(dict.fromkeys(identifiers))
            tool['identifiers'] = identifiers
            print(identifiers)
    except Exception as e:
        print("Error reading -- " + key + " Error -- " + str(url))

    print(tool['home_url'])
    tools[key] = tool

yaml.indent(mapping=4, sequence=6, offset=2)
with open('missing_annotations.yaml', 'w') as outfile:
    yaml.dump(tools, outfile)
